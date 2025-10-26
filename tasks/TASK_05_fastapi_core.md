# TASK 05: FastAPI Core Endpoints (Vanna Integration)

**Status**: ✅ Completed
**Estimated Time**: 6-8 hours
**Dependencies**: TASK 02 (DetomoVanna), TASK 04 (Training data loaded)
**Phase**: 3 - API Layer (Core)

---

## OVERVIEW

Extend the existing FastAPI `claude_agent_server.py` with Vanna API endpoints for querying and training.

**Architecture Decision**: Instead of creating a separate Flask server, we consolidate all endpoints into one FastAPI server for better performance and maintainability.

**Reference**: PRD Section 4.5

---

## OBJECTIVES

1. Extend `claude_agent_server.py` with Vanna functionality
2. Initialize DetomoVanna at server startup
3. Implement `/api/v0/query` endpoint (all-in-one: NL → SQL → results → chart)
4. Implement `/api/v0/train` endpoint (add training data)
5. Implement `/api/v0/health` endpoint (comprehensive health check)
6. Keep existing `/generate` and `/health` endpoints for internal use
7. Write integration tests

---

## ARCHITECTURE

```
┌──────────────────────────────────────────────────────────┐
│         FastAPI Unified Server (port 8000)               │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  INTERNAL ENDPOINTS (Vanna calls internally):            │
│  ├─ POST /generate          - LLM inference endpoint     │
│  └─ GET  /health            - LLM service health         │
│                                                           │
│  PUBLIC API ENDPOINTS (User/Frontend calls):             │
│  ├─ POST /api/v0/query      - Simple: Question → Result │
│  ├─ POST /api/v0/train      - Add training data         │
│  └─ GET  /api/v0/health     - Full API health check     │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

**Key Points:**
- **Same server, different purposes**: `/generate` is for Vanna internal, `/api/v0/*` is for users
- **DetomoVanna calls `/generate`**: When you call `vn.generate_sql()`, it internally POSTs to `http://localhost:8000/generate`
- **Frontend calls `/api/v0/*`**: User-facing endpoints with complete functionality

---

## IMPLEMENTATION

Update `claude_agent_server.py`:

### Step 1: Add Imports

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock
from src.detomo_vanna import DetomoVanna
import logging
import uvicorn
from typing import Optional, Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Step 2: Add Request/Response Models for Public API

```python
# Existing models: GenerateRequest, GenerateResponse, HealthResponse

# New models for public API
class QueryRequest(BaseModel):
    question: str = Field(..., description="Natural language question")
    language: Optional[str] = Field(default="en", description="Language: 'en' or 'jp'")

class QueryResponse(BaseModel):
    question: str
    sql: str
    results: List[Dict[str, Any]]
    columns: List[str]
    visualization: Optional[Dict[str, Any]] = None
    row_count: int

class TrainRequest(BaseModel):
    ddl: Optional[str] = None
    documentation: Optional[str] = None
    question: Optional[str] = None
    sql: Optional[str] = None

class TrainResponse(BaseModel):
    status: str
    message: str

class APIHealthResponse(BaseModel):
    status: str
    service: str
    version: str
    llm_endpoint: str
    database: str
    training_data_count: int
```

### Step 3: Initialize DetomoVanna at Startup

```python
# Global variable for Vanna instance
vn: Optional[DetomoVanna] = None

@app.on_event("startup")
async def startup_event():
    """Initialize DetomoVanna and connect to database"""
    global vn

    logger.info("Claude Agent SDK server starting...")
    logger.info("Using Claude Code authentication")
    logger.info("Initializing DetomoVanna...")

    try:
        # Initialize Vanna
        vn = DetomoVanna(config={
            "path": "./detomo_vectordb",
            "client": "persistent",
            "agent_endpoint": "http://localhost:8000/generate",
            "model": "claude-sonnet-4-5"
        })

        # Connect to database
        vn.connect_to_sqlite("data/chinook.db")

        # Verify training data
        training_data = vn.get_training_data()
        logger.info(f"✓ DetomoVanna initialized with {len(training_data)} training items")
        logger.info("API documentation available at http://localhost:8000/docs")

    except Exception as e:
        logger.error(f"Failed to initialize DetomoVanna: {e}")
        raise
```

### Step 4: Add Public API Endpoints

```python
# ============================================
# PUBLIC API ENDPOINTS
# ============================================

@app.post("/api/v0/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    All-in-one endpoint: Natural language → SQL → Results → Visualization

    This is a simple endpoint for straightforward queries.
    For advanced workflows with caching, see TASK_07 endpoints.

    Example:
        POST /api/v0/query
        {
            "question": "How many customers are there?",
            "language": "en"
        }

        Response:
        {
            "question": "How many customers are there?",
            "sql": "SELECT COUNT(*) FROM customers",
            "results": [{"count": 59}],
            "columns": ["count"],
            "visualization": {...},
            "row_count": 1
        }
    """

    if not vn:
        raise HTTPException(status_code=500, detail="DetomoVanna not initialized")

    if not request.question or len(request.question.strip()) == 0:
        raise HTTPException(status_code=400, detail="Missing or empty 'question' field")

    logger.info(f"Received query: {request.question}")

    try:
        # Generate SQL
        sql = vn.generate_sql(request.question)
        logger.info(f"Generated SQL: {sql}")

        # Execute SQL
        df = vn.run_sql(sql)

        # Generate visualization (optional)
        fig_json = None
        try:
            fig = vn.get_plotly_figure(sql=sql, df=df, question=request.question)
            if fig:
                fig_json = fig.to_json()
        except Exception as e:
            logger.warning(f"Could not generate visualization: {e}")

        # Convert DataFrame to dict
        results = df.to_dict(orient='records')
        columns = df.columns.tolist()

        logger.info(f"Query successful - {len(results)} rows returned")

        return QueryResponse(
            question=request.question,
            sql=sql,
            results=results,
            columns=columns,
            visualization=fig_json,
            row_count=len(results)
        )

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.post("/api/v0/train", response_model=TrainResponse)
async def train(request: TrainRequest):
    """
    Add training data to Vanna

    You can add:
    - DDL (CREATE TABLE statements)
    - Documentation (table/column descriptions)
    - Q&A pairs (question + SQL examples)

    Examples:
        # Add DDL
        POST /api/v0/train
        {"ddl": "CREATE TABLE customers (...)"}

        # Add documentation
        POST /api/v0/train
        {"documentation": "Customers table contains..."}

        # Add Q&A pair
        POST /api/v0/train
        {"question": "How many customers?", "sql": "SELECT COUNT(*) FROM customers"}
    """

    if not vn:
        raise HTTPException(status_code=500, detail="DetomoVanna not initialized")

    try:
        if request.ddl:
            vn.train(ddl=request.ddl)
            return TrainResponse(status="success", message="DDL added to training data")

        elif request.documentation:
            vn.train(documentation=request.documentation)
            return TrainResponse(status="success", message="Documentation added to training data")

        elif request.question and request.sql:
            vn.train(question=request.question, sql=request.sql)
            return TrainResponse(status="success", message="Q&A pair added to training data")

        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid training data format. Provide 'ddl', 'documentation', or ('question' + 'sql')"
            )

    except Exception as e:
        logger.error(f"Error adding training data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")


@app.get("/api/v0/health", response_model=APIHealthResponse)
async def api_health():
    """
    Comprehensive health check for the entire API

    Checks:
    - Server status
    - DetomoVanna initialization
    - Database connection
    - Training data loaded
    - LLM endpoint available
    """

    try:
        # Check Vanna initialized
        if not vn:
            raise HTTPException(status_code=503, detail="DetomoVanna not initialized")

        # Check training data
        training_data = vn.get_training_data()
        training_count = len(training_data)

        # Check database connection
        try:
            vn.run_sql("SELECT 1")
            db_status = "data/chinook.db - Connected"
        except:
            db_status = "data/chinook.db - Disconnected"
            raise HTTPException(status_code=503, detail="Database not connected")

        return APIHealthResponse(
            status="healthy",
            service="Detomo SQL AI API",
            version="2.0.0",
            llm_endpoint="http://localhost:8000/generate",
            database=db_status,
            training_data_count=training_count
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")
```

---

## SUCCESS CRITERIA

- [ ] `claude_agent_server.py` extended with Vanna endpoints
- [ ] DetomoVanna initialized at server startup
- [ ] API runs on http://localhost:8000
- [ ] `/api/v0/query` endpoint works (NL → SQL → Results)
- [ ] `/api/v0/train` endpoint works (add training data)
- [ ] `/api/v0/health` endpoint works (comprehensive check)
- [ ] Existing `/generate` endpoint still works for Vanna internal use
- [ ] CORS enabled for all endpoints
- [ ] Error handling comprehensive
- [ ] Integration tests passing

---

## TESTING

```bash
# Start unified FastAPI server
python claude_agent_server.py

# Test internal LLM endpoint (Vanna uses this)
curl http://localhost:8000/health

curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Generate SQL for: How many customers?", "model": "claude-sonnet-4-5"}'

# Test public API endpoints (User/Frontend uses these)
curl http://localhost:8000/api/v0/health

curl -X POST http://localhost:8000/api/v0/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How many customers are there?"}'

curl -X POST http://localhost:8000/api/v0/train \
  -H "Content-Type: application/json" \
  -d '{"question": "Count customers", "sql": "SELECT COUNT(*) FROM customers"}'
```

Create `tests/integration/test_api_core.py`:

```python
import pytest
import requests
from time import sleep

BASE_URL = "http://localhost:8000"

def test_api_health():
    """Test comprehensive API health check"""
    response = requests.get(f"{BASE_URL}/api/v0/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["training_data_count"] > 0

def test_query_endpoint():
    """Test query endpoint with simple question"""
    response = requests.post(
        f"{BASE_URL}/api/v0/query",
        json={"question": "How many customers are there?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "sql" in data
    assert "results" in data
    assert len(data["results"]) > 0

def test_train_endpoint_qa():
    """Test adding Q&A pair"""
    response = requests.post(
        f"{BASE_URL}/api/v0/train",
        json={
            "question": "Test question",
            "sql": "SELECT 1"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

def test_internal_generate_still_works():
    """Test that internal /generate endpoint still works"""
    response = requests.post(
        f"{BASE_URL}/generate",
        json={
            "prompt": "SELECT COUNT(*) FROM customers",
            "model": "claude-sonnet-4-5"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
```

---

## NOTES

### Why Unified FastAPI Server?

**Advantages:**
1. **Single process**: Easier deployment and management
2. **Better performance**: FastAPI is faster than Flask, supports async
3. **Consistent framework**: All endpoints use same framework and middleware
4. **Resource efficient**: One server instead of two saves memory
5. **Simplified architecture**: Frontend only needs to connect to one port

**Trade-offs:**
- Differs from original PRD (which specified Flask)
- But architecturally superior and aligns with FastAPI choice for LLM endpoint

### Endpoint Separation

- **Internal endpoints** (`/generate`, `/health`): Called by Vanna/DetomoVanna internally
- **Public endpoints** (`/api/v0/*`): Called by user, frontend, or external clients
- Both run on same server (port 8000) but serve different purposes

---

## REFERENCES

- **PRD Section 4.5**: API Architecture (updated to reflect unified server)
- **Existing**: `claude_agent_server.py` (TASK_01)
- **Dependency**: `src/detomo_vanna.py` (TASK_02)

---

**Last Updated**: 2025-10-26
**Architecture Decision**: Unified FastAPI server approved
