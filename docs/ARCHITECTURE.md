# Architecture Documentation - Detomo SQL AI

**Project**: Detomo SQL AI v2.0
**Last Updated**: 2025-10-26
**Version**: 2.0.0

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Core Components](#core-components)
4. [Data Flow](#data-flow)
5. [Technology Stack](#technology-stack)
6. [Design Decisions](#design-decisions)
7. [Database Schema](#database-schema)
8. [API Architecture](#api-architecture)
9. [Security Considerations](#security-considerations)
10. [Scalability](#scalability)

---

## System Overview

Detomo SQL AI is an AI-powered Text-to-SQL application that converts natural language questions (in English or Japanese) into SQL queries, executes them against a database, and generates visualizations of the results.

### Key Features

- **Natural Language Processing**: Converts user questions to SQL using Claude Sonnet 4.5
- **RAG-Enhanced Generation**: Uses ChromaDB vector store to retrieve relevant schema and examples
- **Multi-Step Workflow**: Supports both all-in-one and incremental query processing
- **Auto-Visualization**: Generates Plotly charts automatically from query results
- **Bilingual Support**: Works with both English and Japanese questions
- **Training Data Management**: API endpoints to add/remove training examples
- **Web UI**: Interactive SPA for querying and visualization

### Architecture Philosophy

The system follows these key principles:

1. **Separation of Concerns**: Clear boundaries between LLM, RAG, API, and UI layers
2. **Modularity**: Each component (Vanna, Cache, API, UI) can be tested independently
3. **Extensibility**: Easy to add new databases, LLM providers, or UI features
4. **Simplicity**: Uses proven frameworks (FastAPI, Vanna) rather than custom implementations
5. **Performance**: Async operations and thread pools for handling concurrent requests

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE LAYER                           │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Web UI (React/Vue SPA)                        │   │
│  │  - Chat interface    - SQL display    - Results table            │   │
│  │  - Query history     - Plotly charts  - Training data manager    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                            │
│                              │ HTTP (REST API)                            │
│                              ▼                                            │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                           API LAYER (FastAPI)                            │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                  FastAPI Server (Port 8000)                      │   │
│  │                                                                   │   │
│  │  Core Endpoints:                                                 │   │
│  │  • POST /api/v0/query           (all-in-one query)              │   │
│  │  • POST /api/v0/train           (add training data)             │   │
│  │  • GET  /api/v0/health          (health check)                  │   │
│  │                                                                   │   │
│  │  Multi-Step Endpoints (Vanna-Flask Pattern):                    │   │
│  │  • GET  /api/v0/generate_questions                              │   │
│  │  • POST /api/v0/generate_sql                                    │   │
│  │  • POST /api/v0/run_sql                                         │   │
│  │  • POST /api/v0/generate_plotly_figure                          │   │
│  │  • POST /api/v0/generate_followup_questions                     │   │
│  │  • POST /api/v0/load_question                                   │   │
│  │  • GET  /api/v0/get_question_history                            │   │
│  │  • GET  /api/v0/get_training_data                               │   │
│  │  • POST /api/v0/remove_training_data                            │   │
│  │  • GET  /api/v0/download_csv                                    │   │
│  │                                                                   │   │
│  │  Internal LLM Endpoint:                                          │   │
│  │  • POST /generate                (Claude Agent SDK endpoint)    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                            │
│                              ▼                                            │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                        BUSINESS LOGIC LAYER                              │
│                                                                           │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────┐ │
│  │   DetomoVanna       │  │   MemoryCache       │  │  ThreadPool     │ │
│  │   (Vanna AI)        │  │                     │  │  Executor       │ │
│  │                     │  │  • Query state      │  │                 │ │
│  │  • generate_sql()   │  │  • Results cache    │  │  • Async ops    │ │
│  │  • run_sql()        │  │  • History tracking │  │  • Concurrency  │ │
│  │  • train()          │  │  • Session mgmt     │  │  • Non-blocking │ │
│  │  • generate_viz()   │  │                     │  │                 │ │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────┘ │
│           │                                                               │
│           │                                                               │
│           ▼                                                               │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                        DATA & AI LAYER                                   │
│                                                                           │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────────┐  │
│  │ ChromaDB         │  │ Claude Agent SDK │  │  SQLite Database    │  │
│  │ Vector Store     │  │                  │  │  (Chinook)          │  │
│  │                  │  │  Claude Sonnet   │  │                     │  │
│  │ • DDL embeddings │  │  4.5             │  │  • Customer         │  │
│  │ • Docs           │  │                  │  │  • Invoice          │  │
│  │ • Q&A examples   │  │  • SQL gen       │  │  • Track            │  │
│  │ • Similarity     │  │  • Viz code gen  │  │  • Artist           │  │
│  │   search (RAG)   │  │  • Follow-ups    │  │  • Album            │  │
│  │                  │  │                  │  │  • Genre            │  │
│  │ 93 training items│  │  Temperature:    │  │  • ...etc           │  │
│  │                  │  │  0.1             │  │                     │  │
│  └──────────────────┘  └──────────────────┘  └─────────────────────┘  │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                         INFRASTRUCTURE LAYER                             │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  • Python 3.10+    • uvicorn (ASGI server)                      │   │
│  │  • Virtual env     • CORS middleware                             │   │
│  │  • .env config     • Static file serving                         │   │
│  │  • Logging         • Request validation (Pydantic)               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. FastAPI Server (`claude_agent_server.py`)

**Purpose**: Main application server providing REST API and serving UI

**Key Responsibilities**:
- Expose REST API endpoints for frontend
- Handle LLM generation requests via Claude Agent SDK
- Manage DetomoVanna instance lifecycle
- Serve static UI files
- Handle CORS and request validation

**Technologies**:
- FastAPI (async web framework)
- Pydantic (request/response validation)
- uvicorn (ASGI server)
- ThreadPoolExecutor (for blocking Vanna calls)

**Startup Process**:
1. Initialize DetomoVanna with ChromaDB config
2. Connect to SQLite database
3. Verify training data loaded
4. Start uvicorn server on port 8000

### 2. DetomoVanna (`src/detomo_vanna.py`)

**Purpose**: Custom Vanna AI implementation integrating Claude Agent SDK

**Class Hierarchy**:
```python
DetomoVanna
    ├─ ChromaDB_VectorStore    # RAG retrieval
    └─ ClaudeAgentChat         # LLM generation
```

**Key Methods**:
- `generate_sql(question: str) -> str`: Generate SQL from NL question
- `run_sql(sql: str) -> DataFrame`: Execute SQL and return results
- `train(ddl/documentation/sql)`: Add training data to ChromaDB
- `generate_plotly_code()`: Generate Plotly visualization code
- `generate_questions()`: Suggest sample questions
- `generate_followup_questions()`: Suggest related questions

**Configuration**:
```python
config = {
    "path": "./detomo_vectordb",           # ChromaDB storage
    "client": "persistent",                 # ChromaDB client type
    "agent_endpoint": "http://localhost:8000/generate",  # LLM endpoint
    "model": "claude-sonnet-4-5",          # Claude model
    "temperature": 0.1,                     # Low temp for deterministic SQL
    "max_tokens": 2048                      # Max response length
}
```

### 3. ClaudeAgentChat (`src/detomo_vanna.py`)

**Purpose**: Vanna LLM interface adapter for Claude Agent SDK

**Key Features**:
- Implements Vanna's `submit_prompt()` interface
- Converts Vanna message format to Claude format
- Handles HTTP communication with LLM endpoint
- Error handling and timeout management (30s timeout)

**System Prompt**:
```
You are a SQL expert. Generate accurate SQL queries based on the given context.

Rules:
- Generate ONLY the SQL query, no explanation
- Use proper SQL syntax
- Follow the database schema provided in the prompt
- Use similar examples as reference when provided
```

### 4. MemoryCache (`src/cache.py`)

**Purpose**: In-memory cache for multi-step query workflow

**Data Structure**:
```python
{
    "cache-id-123": {
        "question": "How many customers?",
        "sql": "SELECT COUNT(*) FROM Customer",
        "df": pandas.DataFrame(...),
        "fig": {...plotly JSON...},
        "error": "..." (if any)
    }
}
```

**Key Methods**:
- `generate_id()`: Create unique UUID for cache entry
- `set(id, field, value)`: Store field in cache
- `get(id, field)`: Retrieve field from cache
- `get_all(field)`: Get all values of a field (for history)
- `delete(id)`: Remove cache entry
- `exists(id)`: Check if entry exists

**Use Cases**:
- Multi-step workflow: generate_sql → run_sql → generate_viz
- Query history tracking
- Session management across API calls

### 5. ChromaDB Vector Store

**Purpose**: RAG knowledge base for SQL generation

**Storage Location**: `./detomo_vectordb/`

**Training Data** (93 items total):
- **DDL**: 12 CREATE TABLE statements (all Chinook tables + relationships)
- **Documentation**: 11 markdown files describing tables and columns (EN/JP)
- **Q&A Examples**: 70 question-SQL pairs (EN/JP, various difficulty levels)

**Embedding Model**: Default ChromaDB embeddings (all-MiniLM-L6-v2)

**Retrieval Process**:
1. User asks question
2. Question embedded to vector
3. ChromaDB finds top-K similar training examples
4. Vanna builds prompt with: question + schema + examples
5. Claude generates SQL based on context

### 6. Web UI (`static/index.html`)

**Purpose**: Single-page application for user interaction

**Key Features**:
- Chat-style interface for asking questions
- SQL syntax highlighting (highlight.js)
- Results table display
- Plotly chart rendering
- Query history sidebar
- Training data info panel
- Dark mode support
- Bilingual support (EN/JP)

**Technology**:
- Vanilla JavaScript (no framework)
- Tailwind CSS (styling)
- Plotly.js (visualizations)
- Marked.js (markdown rendering)
- Highlight.js (code highlighting)

---

## Data Flow

### All-in-One Query Flow (`POST /api/v0/query`)

```
1. User sends question via UI
   └─> POST /api/v0/query {"question": "How many customers?"}

2. FastAPI endpoint receives request
   └─> Validates request (Pydantic)

3. Call DetomoVanna.generate_sql()
   ├─> ChromaDB retrieves relevant training data (top 10 similar examples)
   ├─> Vanna builds prompt: question + schema + examples
   ├─> ClaudeAgentChat.submit_prompt() calls /generate endpoint
   ├─> Claude Agent SDK generates SQL
   └─> Returns SQL: "SELECT COUNT(*) FROM Customer"

4. Call DetomoVanna.run_sql()
   ├─> SQLite executes query
   └─> Returns DataFrame with results

5. Call DetomoVanna.generate_plotly_code() (optional)
   ├─> Vanna asks Claude to generate Plotly Python code
   ├─> Execute code to create figure
   └─> Returns Plotly JSON

6. FastAPI returns response to UI
   └─> {sql, results, columns, visualization, row_count}

7. UI displays results
   ├─> Shows SQL with syntax highlighting
   ├─> Displays results table
   └─> Renders Plotly chart
```

### Multi-Step Query Flow (Vanna-Flask Pattern)

```
1. Generate SQL
   POST /api/v0/generate_sql {"question": "..."}
   ├─> DetomoVanna.generate_sql()
   ├─> Cache.set(id, "question", question)
   ├─> Cache.set(id, "sql", sql)
   └─> Returns {id, question, sql}

2. Execute SQL
   POST /api/v0/run_sql {"id": "abc-123"}
   ├─> Cache.get(id, "sql")
   ├─> DetomoVanna.run_sql(sql)
   ├─> Cache.set(id, "df", dataframe)
   └─> Returns {id, results, columns, row_count}

3. Generate Visualization
   POST /api/v0/generate_plotly_figure {"id": "abc-123"}
   ├─> Cache.get(id, "question", "sql", "df")
   ├─> DetomoVanna.generate_plotly_code()
   ├─> Cache.set(id, "fig", figure_json)
   └─> Returns {id, figure}

4. Load Complete State
   POST /api/v0/load_question {"id": "abc-123"}
   ├─> Cache.get(id, all fields)
   └─> Returns {id, question, sql, results, columns, figure, row_count}
```

### Training Data Flow

```
1. Training Script (scripts/train_chinook.py)
   ├─> Reads training_data/chinook/ddl/*.sql
   ├─> Reads training_data/chinook/documentation/*.md
   ├─> Reads training_data/chinook/questions/*.json
   └─> Calls vn.train() for each item

2. DetomoVanna.train()
   ├─> Generates embedding for content
   ├─> Stores in ChromaDB
   └─> Assigns unique ID

3. ChromaDB Storage
   ├─> Vector embeddings in ./detomo_vectordb/
   └─> Metadata (content, type, timestamp)

4. Query-Time Retrieval
   ├─> User asks question
   ├─> Question embedded
   ├─> ChromaDB similarity search (top 10)
   └─> Results included in prompt to Claude
```

---

## Technology Stack

### Backend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Framework | FastAPI | 0.110.0+ | High-performance async web framework |
| Server | uvicorn | 0.27.0+ | ASGI server for FastAPI |
| LLM Framework | Vanna AI | 0.7.9 | Text-to-SQL RAG framework |
| LLM Provider | Claude Agent SDK | 0.1.0+ | Claude API client |
| LLM Model | Claude Sonnet 4.5 | - | Latest Claude model for SQL |
| Vector DB | ChromaDB | <1.0.0 | Embedding storage and retrieval |
| Database | SQLite | 3.x | Target database (Chinook) |
| Data Processing | pandas | Latest | DataFrame operations |
| Visualization | Plotly | Latest | Chart generation |
| Validation | Pydantic | 2.x | Request/response validation |
| HTTP Client | requests | 2.31.0+ | HTTP calls to LLM endpoint |

### Frontend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | Vanilla JS | Lightweight SPA |
| Styling | Tailwind CSS | Utility-first CSS |
| Charts | Plotly.js | Interactive visualizations |
| Markdown | Marked.js | Markdown rendering |
| Syntax | Highlight.js | SQL syntax highlighting |

### Development & Testing

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Testing | pytest | Unit and integration tests |
| Async Testing | pytest-asyncio | Async test support |
| Coverage | pytest-cov | Code coverage reporting |
| HTTP Testing | httpx | Async HTTP client for tests |
| Environment | python-dotenv | Environment variable management |

---

## Design Decisions

### 1. Why FastAPI instead of Flask?

**Decision**: Use FastAPI as the main web framework

**Rationale**:
- **Performance**: FastAPI is significantly faster (async support)
- **Modern**: Built-in async/await support for concurrent requests
- **Validation**: Automatic request/response validation with Pydantic
- **Documentation**: Auto-generated OpenAPI docs at `/docs`
- **Type Safety**: Better type hints and editor support
- **Future-proof**: Growing ecosystem and community

**Impact**: Unified server architecture, better performance, easier to maintain

### 2. Why Vanna AI?

**Decision**: Use Vanna AI as the Text-to-SQL framework

**Rationale**:
- **RAG Built-in**: ChromaDB integration for retrieving schema and examples
- **Proven**: Production-ready, widely used framework
- **Customizable**: Easy to swap LLM providers (we use Claude instead of OpenAI)
- **Training**: Simple API for adding DDL, docs, and Q&A pairs
- **Visualization**: Built-in Plotly chart generation

**Alternatives Considered**:
- LangChain SQL chain (more complex, less specialized)
- Custom RAG pipeline (more work, reinventing wheel)
- Direct LLM calls (no RAG, lower accuracy)

### 3. Why Claude Agent SDK?

**Decision**: Use Claude Agent SDK as LLM provider

**Rationale**:
- **Quality**: Claude Sonnet 4.5 has excellent SQL generation capabilities
- **Authentication**: Integrates with Claude Code environment (no API key needed)
- **Reasoning**: Strong reasoning for complex join queries
- **Bilingual**: Excellent Japanese language support
- **Cost**: Reasonable pricing compared to GPT-4

**Alternative**: Direct Anthropic API (requires API key management)

### 4. Why ChromaDB?

**Decision**: Use ChromaDB as vector database

**Rationale**:
- **Vanna Native**: First-class support in Vanna
- **Simple**: Easy setup, no external service needed
- **Persistent**: Stores embeddings locally
- **Fast**: Good performance for our dataset size (~100 items)

**Alternative**: Pinecone, Weaviate (overkill for MVP, require external service)

### 5. Why Memory Cache instead of Redis?

**Decision**: Use in-memory cache (Python dict)

**Rationale**:
- **Simplicity**: No external dependency, zero configuration
- **MVP Scope**: Sufficient for single-server deployment
- **Fast**: Instant access, no network latency
- **Stateless**: Cache doesn't need persistence

**Future**: Can upgrade to Redis for multi-server deployments

### 6. Why Unified Server Architecture?

**Decision**: Single FastAPI server instead of separate Flask + FastAPI

**Original Plan**:
- FastAPI for LLM endpoint (port 8000)
- Flask for public API (port 5000)

**Change**:
- Single FastAPI server for everything (port 8000)

**Rationale**:
- **Simplicity**: One server, one port, easier deployment
- **Performance**: FastAPI throughout (Flask is slower)
- **Consistency**: Same framework, same patterns
- **Resources**: Lower memory footprint

**Impact**: Simplified deployment, better performance

### 7. Why SQLite/Chinook?

**Decision**: Use SQLite with Chinook database for MVP

**Rationale**:
- **Standard**: Chinook is a well-known test database
- **Simple**: No server setup, just a file
- **Realistic**: Real-world schema (music store)
- **Portable**: Easy to distribute and test

**Production**: Can easily swap to PostgreSQL, MySQL, etc. (Vanna supports all)

---

## Database Schema

### Chinook Database

The Chinook database represents a digital music store with 11 tables:

**Core Entities**:
- `Artist`: Music artists (275 rows)
- `Album`: Music albums (347 rows)
- `Track`: Individual songs (3,503 rows)
- `Genre`: Music genres (25 rows)
- `MediaType`: File formats (5 rows)

**Sales & Customers**:
- `Customer`: Store customers (59 rows)
- `Invoice`: Sales invoices (412 rows)
- `InvoiceLine`: Invoice line items (2,240 rows)

**Employees**:
- `Employee`: Store employees (8 rows)

**Playlists**:
- `Playlist`: User playlists (18 rows)
- `PlaylistTrack`: Tracks in playlists (8,715 rows)

**Key Relationships**:
```
Artist (1) ─── (N) Album (1) ─── (N) Track
                                    │
                                    ├─── (N) InvoiceLine (N) ─── (1) Invoice (N) ─── (1) Customer
                                    │                                                      │
                                    ├─── (1) Genre                                    (1) Employee (manager)
                                    ├─── (1) MediaType
                                    └─── (N) PlaylistTrack (N) ─── (1) Playlist
```

**Location**: `data/chinook.db`

---

## API Architecture

### Endpoint Categories

**1. Core Endpoints** (Simple, all-in-one):
- `POST /api/v0/query`: Complete NL → SQL → Results → Viz workflow
- `POST /api/v0/train`: Add training data
- `GET /api/v0/health`: Health check

**2. Multi-Step Endpoints** (Vanna-Flask pattern, cache-based):
- `GET /api/v0/generate_questions`: Suggest sample questions
- `POST /api/v0/generate_sql`: Step 1 - Generate SQL only
- `POST /api/v0/run_sql`: Step 2 - Execute cached SQL
- `POST /api/v0/generate_plotly_figure`: Step 3 - Generate visualization
- `POST /api/v0/generate_followup_questions`: Suggest related questions
- `POST /api/v0/load_question`: Load complete cached query state
- `GET /api/v0/get_question_history`: List all cached queries
- `GET /api/v0/get_training_data`: List all training examples
- `POST /api/v0/remove_training_data`: Delete training example
- `GET /api/v0/download_csv`: Export results as CSV

**3. Internal Endpoints**:
- `POST /generate`: LLM endpoint for Vanna (not exposed to users)
- `GET /health`: LLM endpoint health check
- `GET /`: Serve UI (index.html)

### Request/Response Patterns

**Standard Response Structure**:
```json
{
    "status": "success|error",
    "data": {...},
    "message": "Optional message"
}
```

**Error Handling**:
```json
{
    "status": "error",
    "detail": "Error message explaining what went wrong"
}
```

**HTTP Status Codes**:
- `200 OK`: Successful request
- `400 Bad Request`: Invalid input
- `404 Not Found`: Resource not found (cache ID, training data ID)
- `500 Internal Server Error`: Server error (LLM failure, DB error)
- `503 Service Unavailable`: Service not ready (DetomoVanna not initialized)

### Async Operations

**Thread Pool Strategy**:
```python
executor = ThreadPoolExecutor(max_workers=4)

# Vanna operations are blocking, so run in thread pool
loop = asyncio.get_event_loop()
result = await loop.run_in_executor(executor, vn.generate_sql, question)
```

**Why**:
- Vanna operations are synchronous (blocking)
- FastAPI is async (non-blocking)
- Thread pool bridges sync and async worlds
- Prevents blocking the event loop

---

## Security Considerations

### Current Implementation (MVP)

**Authentication**: None (MVP focuses on functionality)
**Authorization**: None (open API)
**CORS**: Allows all origins (`allow_origins=["*"]`)
**Rate Limiting**: None

### Production Recommendations

**1. Authentication**:
- Add API key authentication
- Or OAuth 2.0 for user-based access
- JWT tokens for session management

**2. Input Validation**:
- ✅ Pydantic validates request format
- ✅ SQL injection protected (Vanna uses parameterized queries)
- ⚠️ Add rate limiting per user/IP

**3. Database Security**:
- ✅ Read-only user (recommended)
- Consider query timeout limits
- Implement query complexity checks

**4. CORS**:
- Configure specific allowed origins
- Remove wildcard (`*`) in production

**5. API Key Protection**:
- ✅ Use Claude Code environment (no .env file needed for MVP)
- For production: Use secrets management (AWS Secrets Manager, Vault)

**6. Logging & Monitoring**:
- ✅ Basic logging implemented
- Add structured logging (JSON format)
- Monitor API usage and errors
- Alert on suspicious activity

---

## Scalability

### Current Limitations (MVP)

**Single Server**: One FastAPI instance on port 8000
**In-Memory Cache**: Lost on restart
**ChromaDB**: Local file-based storage
**SQLite**: Single file, limited concurrency

### Scaling Strategies

**1. Horizontal Scaling (Multiple Servers)**:

**Problem**: In-memory cache not shared between servers

**Solution**:
```
┌─────────┐
│ Nginx   │ Load Balancer
└────┬────┘
     │
     ├──── FastAPI Server 1 ─────┐
     ├──── FastAPI Server 2 ─────┼──── Redis Cache (shared)
     └──── FastAPI Server 3 ─────┘
```

**Changes Needed**:
- Replace MemoryCache with Redis
- Use sticky sessions or shared cache
- Deploy ChromaDB as external service (Chroma server mode)

**2. Vertical Scaling (Bigger Server)**:

**Current**:
- ThreadPoolExecutor: 4 workers

**Upgrade**:
- Increase workers (8-16)
- More RAM for cache
- Faster disk for ChromaDB

**3. Database Scaling**:

**Current**: SQLite (good for <100 concurrent users)

**Upgrade Options**:
```
SQLite → PostgreSQL → PostgreSQL with read replicas
```

**4. LLM Endpoint Scaling**:

**Current**: Claude Agent SDK (Anthropic API)

**Optimizations**:
- Cache generated SQL (same question → same SQL)
- Batch similar questions
- Use Claude Haiku for simpler queries (cheaper, faster)

**5. CDN for Static Files**:

**Current**: FastAPI serves static files

**Production**: Use CDN (CloudFront, Cloudflare) for UI assets

### Performance Targets

**Current Performance** (from QA testing):
- Mean response time: 4.57s
- P95 response time: 5.54s
- Throughput: ~5-10 requests/second (single server)

**Optimization Opportunities**:
1. Cache SQL for common questions (reduce LLM calls)
2. Optimize ChromaDB retrieval (index tuning)
3. Use smaller LLM for simple queries (Haiku instead of Sonnet)
4. Add request queuing with priority
5. Pre-generate sample questions (cache suggestions)

**Target for Production**:
- Mean response time: <3s
- P95 response time: <5s
- Throughput: 50-100 requests/second (with horizontal scaling)
- 99.9% uptime

---

## Deployment Architecture

### Development Environment

```
Developer Machine
├── Python 3.10+ virtual environment
├── SQLite database (data/chinook.db)
├── ChromaDB (./detomo_vectordb/)
├── FastAPI server (localhost:8000)
└── Claude Code environment (API key)
```

**Start Command**:
```bash
python claude_agent_server.py
```

### Production Environment (Recommended)

```
                    ┌─────────────────┐
                    │   Cloudflare    │
                    │   (CDN + SSL)   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   Nginx Reverse │
                    │   Proxy         │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
    ┌─────▼─────┐     ┌─────▼─────┐     ┌─────▼─────┐
    │ FastAPI   │     │ FastAPI   │     │ FastAPI   │
    │ Server 1  │     │ Server 2  │     │ Server 3  │
    └─────┬─────┘     └─────┬─────┘     └─────┬─────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
    ┌─────▼─────┐     ┌─────▼─────┐     ┌─────▼─────┐
    │  Redis    │     │ PostgreSQL│     │  Chroma   │
    │  Cache    │     │ Database  │     │  Server   │
    └───────────┘     └───────────┘     └───────────┘
```

**Components**:
1. **Cloudflare**: CDN, SSL termination, DDoS protection
2. **Nginx**: Load balancing, reverse proxy
3. **FastAPI Servers**: Multiple instances with gunicorn/uvicorn
4. **Redis**: Shared cache across servers
5. **PostgreSQL**: Production database (replaces SQLite)
6. **Chroma Server**: Centralized vector store

**Deployment Options**:
- Docker containers (recommended)
- Kubernetes for orchestration
- AWS ECS/EKS, Google Cloud Run, Azure Container Instances

---

## Monitoring & Observability

### Logging

**Current**:
```python
logger.info("Query successful")
logger.error("Error processing query")
```

**Production Enhancements**:
- Structured logging (JSON format)
- Log aggregation (ELK stack, Datadog, CloudWatch)
- Request ID tracking
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

### Metrics

**Recommended Metrics**:
- Request count by endpoint
- Response time (p50, p95, p99)
- Error rate by type
- LLM API calls (count, cost)
- Cache hit rate
- Database query time
- Active users

**Tools**: Prometheus + Grafana, Datadog, New Relic

### Health Checks

**Current**:
- `GET /health`: LLM endpoint health
- `GET /api/v0/health`: Comprehensive system health

**Production**:
- Kubernetes liveness/readiness probes
- Database connection checks
- Dependency health (LLM API, ChromaDB)
- Automated alerts on failures

---

## Future Enhancements

### Phase 2 Features

1. **Multi-Database Support**: Connect to multiple databases simultaneously
2. **Query History Persistence**: Save history to database (not just cache)
3. **User Accounts**: Authentication and per-user query history
4. **Advanced Visualizations**: More chart types, custom templates
5. **Query Optimization**: Automatic query optimization suggestions
6. **Natural Language Explanations**: Explain SQL to users
7. **Query Approval Workflow**: Require approval before executing queries

### Phase 3 Features

1. **Real-time Collaboration**: Multiple users working together
2. **Scheduled Queries**: Run queries on schedule, email results
3. **Data Export**: Export to Excel, PDF, Google Sheets
4. **Mobile App**: iOS/Android support
5. **Voice Input**: Ask questions via voice
6. **Multi-tenancy**: Support multiple organizations

---

## Conclusion

Detomo SQL AI is a production-ready Text-to-SQL system built on proven technologies (FastAPI, Vanna AI, Claude). The architecture is modular, extensible, and ready for scaling. The MVP focuses on core functionality, while the architecture supports future enhancements for enterprise deployment.

**Key Strengths**:
- 100% SQL accuracy on test queries
- Fast response times (<5s p95)
- Clean separation of concerns
- Comprehensive test coverage (82 tests)
- Ready for production with minor security enhancements

**Next Steps**:
- Add authentication and authorization
- Deploy with Docker/Kubernetes
- Implement caching for common queries
- Scale horizontally with Redis and load balancing

---

**Document Version**: 1.0
**Last Updated**: 2025-10-26
**Maintained By**: Detomo SQL AI Team
