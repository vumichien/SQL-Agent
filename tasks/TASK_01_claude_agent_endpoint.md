# TASK 01: Claude Agent Endpoint Server

**Status**: ⬜ Not Started
**Estimated Time**: 4-6 hours
**Dependencies**: None
**Phase**: 1 - Core Backend Setup

---

## OVERVIEW

Create an HTTP endpoint server using Claude Agent SDK that serves as the LLM backend for Vanna AI. This server receives prompts from Vanna and returns generated SQL text using Claude Sonnet 4.5.

**Key Principle**: This is a simple LLM endpoint - no database access, no tools, just receive prompt → call Claude → return text.

---

## OBJECTIVES

1. Implement FastAPI server with Claude Agent SDK integration
2. Create `/generate` endpoint for SQL generation
3. Create `/health` endpoint for monitoring
4. Handle errors gracefully
5. Test with sample prompts
6. Write unit tests

---

## DEPENDENCIES

### Python Packages

Add to `requirements.txt`:
```
fastapi>=0.110.0
uvicorn>=0.27.0
claude-agent-sdk>=0.1.0
anthropic>=0.40.0
python-dotenv>=1.0.0
```

Install:
```bash
uv pip install fastapi uvicorn claude-agent-sdk anthropic python-dotenv
```

### Environment Variables

Add to `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
```

---

## REQUIREMENTS

### Functional Requirements

1. **FastAPI Server**:
   - Run on `http://localhost:8000`
   - Support CORS for API calls
   - JSON request/response format
   - Automatic API documentation (Swagger UI)

2. **`/generate` Endpoint** (POST):
   - Accept JSON payload with `prompt`, `model`, `temperature`, `max_tokens`
   - Call Claude Agent SDK with the prompt
   - Return JSON response with `text` and `model`
   - Handle timeouts and errors

3. **`/health` Endpoint** (GET):
   - Return server status
   - Include service name and version

### Non-Functional Requirements

1. **Performance**: Response time < 3 seconds for simple queries
2. **Reliability**: Handle API errors gracefully
3. **Logging**: Log all requests and errors
4. **Security**: Validate ANTHROPIC_API_KEY exists

---

## IMPLEMENTATION STEPS

### Step 1: Create Server File

Create `claude_agent_server.py` in project root:

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Claude Agent SDK LLM Endpoint",
    description="LLM endpoint for Vanna AI using Claude Agent SDK",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="The prompt to send to Claude")
    model: str = Field(default="claude-sonnet-4-5", description="Claude model to use")
    temperature: float = Field(default=0.1, ge=0.0, le=1.0, description="Temperature for generation")
    max_tokens: int = Field(default=2048, gt=0, description="Maximum tokens to generate")


class GenerateResponse(BaseModel):
    text: str = Field(..., description="Generated text from Claude")
    model: str = Field(..., description="Model used for generation")


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """
    LLM endpoint for Vanna using Claude Agent SDK.

    Receives prompt from Vanna, uses Claude Agent SDK, returns text.
    No database access, no tools, just simple LLM inference.
    """
    logger.info(f"Received request - Model: {request.model}, Prompt length: {len(request.prompt)}")

    try:
        result = await call_claude_agent(
            request.prompt,
            request.model,
            request.temperature,
            request.max_tokens
        )

        logger.info(f"Generated response - Length: {len(result['text'])}")
        return GenerateResponse(**result)

    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def call_claude_agent(prompt: str, model: str, temperature: float, max_tokens: int) -> dict:
    """
    Call Claude Agent SDK to generate SQL.

    Uses minimal configuration - no tools, no complex system prompt.
    Just basic LLM inference for Vanna.
    """

    # Simple system prompt for SQL generation
    system_prompt = """You are a SQL expert. Generate accurate SQL queries based on the given context.

Rules:
- Generate ONLY the SQL query, no explanation
- Use proper SQL syntax
- Follow the database schema provided in the prompt
- Use similar examples as reference when provided"""

    # Configure Agent SDK with minimal options
    # Note: API key is set via ANTHROPIC_API_KEY environment variable
    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
        model=model,
        permission_mode="bypassPermissions",  # No file access needed
        max_turns=1,  # Single turn - just generate SQL
        allowed_tools=[]  # No tools needed for simple LLM inference
    )

    # Use Agent SDK (API key from environment variable)
    async with ClaudeSDKClient(options=options) as client:

        # Send query to agent
        await client.query(prompt)

        # Collect response
        response_text = ""
        async for message in client.receive_response():
            # Check if it's an AssistantMessage
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    # Extract text from TextBlock
                    if isinstance(block, TextBlock):
                        response_text += block.text

        return {
            "text": response_text.strip(),
            "model": model
        }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        service="Claude Agent SDK LLM Endpoint",
        version="1.0.0"
    )


@app.on_event("startup")
async def startup_event():
    """Validate environment on startup"""
    if not os.getenv("ANTHROPIC_API_KEY"):
        logger.error("ANTHROPIC_API_KEY not found in environment variables!")
        raise RuntimeError("Please set ANTHROPIC_API_KEY in .env file")

    logger.info("Claude Agent SDK server starting...")
    logger.info("API documentation available at http://localhost:8000/docs")
```

### Step 2: Test the Server

#### Start the Server

```bash
uvicorn claude_agent_server:app --host 0.0.0.0 --port 8000 --reload
```

Expected output:
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Claude Agent SDK server starting...
INFO:     API documentation available at http://localhost:8000/docs
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

#### Test Health Endpoint

```bash
curl -X GET http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Claude Agent SDK LLM Endpoint",
  "version": "1.0.0"
}
```

#### Test Generate Endpoint

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Generate SQL to count customers in Customer table",
    "model": "claude-sonnet-4-5",
    "temperature": 0.1
  }'
```

Expected response:
```json
{
  "text": "SELECT COUNT(*) FROM Customer",
  "model": "claude-sonnet-4-5"
}
```

### Step 3: Write Unit Tests

Create `tests/unit/test_agent_endpoint.py`:

```python
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from claude_agent_server import app, call_claude_agent


@pytest.fixture
def client():
    """Create FastAPI test client"""
    return TestClient(app)


def test_health_endpoint(client):
    """Test /health endpoint returns correct status"""
    response = client.get('/health')
    data = response.json()

    assert response.status_code == 200
    assert data['status'] == 'healthy'
    assert data['service'] == 'Claude Agent SDK LLM Endpoint'
    assert data['version'] == '1.0.0'


@patch('claude_agent_server.call_claude_agent')
def test_generate_endpoint_success(mock_call_claude, client):
    """Test /generate endpoint with valid request"""
    # Mock the async function
    mock_call_claude.return_value = {
        "text": "SELECT COUNT(*) FROM Customer",
        "model": "claude-sonnet-4-5"
    }

    response = client.post(
        '/generate',
        json={
            "prompt": "How many customers?",
            "model": "claude-sonnet-4-5",
            "temperature": 0.1,
            "max_tokens": 2048
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert "text" in data
    assert data["text"] == "SELECT COUNT(*) FROM Customer"
    assert data["model"] == "claude-sonnet-4-5"
    mock_call_claude.assert_called_once()


def test_generate_endpoint_missing_prompt(client):
    """Test /generate endpoint with missing prompt"""
    response = client.post(
        '/generate',
        json={
            "model": "claude-sonnet-4-5"
        }
    )

    assert response.status_code == 422  # Validation error in FastAPI
    data = response.json()
    assert "detail" in data


@patch('claude_agent_server.call_claude_agent')
def test_generate_endpoint_error_handling(mock_call_claude, client):
    """Test /generate endpoint handles errors"""
    # Mock an error
    mock_call_claude.side_effect = Exception("API Error")

    response = client.post(
        '/generate',
        json={
            "prompt": "Test prompt",
            "model": "claude-sonnet-4-5"
        }
    )

    data = response.json()

    assert response.status_code == 500
    assert "detail" in data


def test_generate_endpoint_validation(client):
    """Test /generate endpoint input validation"""
    # Test temperature out of range
    response = client.post(
        '/generate',
        json={
            "prompt": "Test",
            "temperature": 1.5  # Invalid: > 1.0
        }
    )
    assert response.status_code == 422

    # Test max_tokens negative
    response = client.post(
        '/generate',
        json={
            "prompt": "Test",
            "max_tokens": -1  # Invalid: < 0
        }
    )
    assert response.status_code == 422


@pytest.mark.asyncio
@patch('claude_agent_server.ClaudeSDKClient')
async def test_call_claude_agent(mock_client_class):
    """Test call_claude_agent function"""
    # Create mock message with TextBlock
    mock_text_block = MagicMock()
    mock_text_block.text = "SELECT COUNT(*) FROM Customer"

    mock_message = MagicMock()
    mock_message.content = [mock_text_block]

    # Create mock client
    mock_client = MagicMock()
    mock_client.query = AsyncMock()
    mock_client.receive_response = AsyncMock(return_value=[mock_message])

    # Mock the async context manager
    mock_client_class.return_value.__aenter__.return_value = mock_client
    mock_client_class.return_value.__aexit__.return_value = AsyncMock()

    # Call the function
    result = await call_claude_agent(
        prompt="Test prompt",
        model="claude-sonnet-4-5",
        temperature=0.1,
        max_tokens=2048
    )

    assert result["text"] == "SELECT COUNT(*) FROM Customer"
    assert result["model"] == "claude-sonnet-4-5"
```

### Step 4: Run Tests

```bash
# Install test dependencies
uv pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/unit/test_agent_endpoint.py -v
```

Expected output:
```
tests/unit/test_agent_endpoint.py::test_health_endpoint PASSED
tests/unit/test_agent_endpoint.py::test_generate_endpoint_success PASSED
tests/unit/test_agent_endpoint.py::test_generate_endpoint_missing_prompt PASSED
tests/unit/test_agent_endpoint.py::test_generate_endpoint_error_handling PASSED
tests/unit/test_agent_endpoint.py::test_generate_endpoint_validation PASSED
tests/unit/test_agent_endpoint.py::test_call_claude_agent PASSED
```

---

## FILE STRUCTURE

After completing this task:

```
SQL-Agent/
├── claude_agent_server.py        # NEW - Main server file
├── .env                          # NEW - Environment variables
├── requirements.txt              # UPDATED - Added dependencies
└── tests/
    └── unit/
        └── test_agent_endpoint.py  # NEW - Unit tests
```

---

## SUCCESS CRITERIA

- [ ] `claude_agent_server.py` created and working
- [ ] Server runs on http://localhost:8000
- [ ] `/health` endpoint returns 200 status
- [ ] `/generate` endpoint accepts JSON and returns SQL
- [ ] Request validation with Pydantic models
- [ ] Error handling for missing/invalid prompt
- [ ] Error handling for API failures
- [ ] ANTHROPIC_API_KEY validation on startup
- [ ] Logging implemented
- [ ] CORS configured properly
- [ ] Swagger UI accessible at http://localhost:8000/docs
- [ ] Unit tests created and passing (≥6 tests)
- [ ] Manual testing with curl successful

---

## TESTING CHECKLIST

### Manual Testing

- [ ] Start server: `uvicorn claude_agent_server:app --host 0.0.0.0 --port 8000 --reload`
- [ ] Test health endpoint: `curl http://localhost:8000/health`
- [ ] Test generate endpoint with valid prompt
- [ ] Test generate endpoint without prompt (should return 422 validation error)
- [ ] Test with missing ANTHROPIC_API_KEY (should fail on startup)
- [ ] Check logs for INFO messages
- [ ] Access Swagger UI at http://localhost:8000/docs
- [ ] Test endpoints via Swagger UI
- [ ] Verify response time < 3 seconds

### Unit Testing

- [ ] Run tests: `pytest tests/unit/test_agent_endpoint.py -v`
- [ ] All tests pass
- [ ] Coverage ≥ 80%: `pytest --cov=claude_agent_server tests/unit/test_agent_endpoint.py`

---

## COMMON ISSUES & SOLUTIONS

### Issue 1: API Key Not Found
**Error**: `WARNING: ANTHROPIC_API_KEY not found`

**Solution**:
```bash
# Create .env file
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" > .env

# Verify it's loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('ANTHROPIC_API_KEY'))"
```

### Issue 2: Import Error for claude_agent_sdk
**Error**: `ModuleNotFoundError: No module named 'claude_agent_sdk'`

**Solution**:
```bash
# Install with uv pip
uv pip install fastapi uvicorn claude-agent-sdk anthropic
```

### Issue 3: Port Already in Use
**Error**: `OSError: [Errno 48] Address already in use`

**Solution**:
```bash
# Find process using port 8000
# Windows:
netstat -ano | findstr :8000
# Unix/macOS:
lsof -i :8000

# Kill the process or use different port
uvicorn claude_agent_server:app --host 0.0.0.0 --port 8001
```

### Issue 4: Uvicorn Not Found
**Error**: `command not found: uvicorn`

**Solution**:
```bash
# Make sure uvicorn is installed
uv pip install uvicorn

# Or use python -m uvicorn
python -m uvicorn claude_agent_server:app --host 0.0.0.0 --port 8000
```

---

## NOTES

### Design Decisions

1. **Why FastAPI?**: Native async support, automatic API docs, better performance, type validation with Pydantic
2. **Why Async?**: Claude Agent SDK requires async/await, FastAPI handles it natively
3. **Why No Tools?**: This endpoint only needs LLM text generation
4. **Why Single Turn?**: Each request is independent, no conversation state
5. **Why Pydantic Models?**: Type safety, automatic validation, better API documentation

### Performance Considerations

- Response time depends on Claude API latency (typically 1-3 seconds)
- No caching implemented yet (can add in future)
- Uvicorn runs with auto-reload in dev mode - use `--workers` for production
- FastAPI is async-native, so it handles concurrent requests efficiently

### Security Considerations

- API key stored in environment variable (not in code)
- Pydantic models provide automatic input validation
- No request size limits (should add in production)
- No rate limiting (should add in production)
- CORS set to allow all origins (configure for production)
- Auto-reload enabled in dev mode (disable in production)

---

## NEXT STEPS

After completing this task:

1. Update [TASK_MASTER.md](../TASK_MASTER.md) - mark TASK 01 as completed
2. Proceed to **TASK 02**: Vanna Custom Class Implementation
3. Keep the server running for TASK 02 testing

---

## REFERENCES

- **Claude Agent SDK Docs**: https://github.com/anthropics/claude-agent-sdk
- **Anthropic API**: https://docs.anthropic.com/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Uvicorn Docs**: https://www.uvicorn.org/
- **Pydantic Docs**: https://docs.pydantic.dev/
- **PRD Section 4.2.3**: Claude Agent SDK Server

---

**Last Updated**: 2025-10-26
