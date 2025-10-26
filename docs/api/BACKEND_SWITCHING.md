# Backend Switching Guide - Detomo SQL AI

## Overview

Detomo SQL AI supports multiple LLM backends with seamless switching capability:

1. **Claude Agent SDK** (Default) - For advanced agent capabilities
2. **Anthropic API** (Fallback) - Direct API calls for simpler use cases

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Flask Application                       │
│                         (app.py)                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   LLM Backend Factory                        │
│                  (backend/llm/factory.py)                    │
└──────────────┬──────────────────────────┬───────────────────┘
               │                          │
       ┌───────▼──────────┐      ┌───────▼──────────┐
       │ ClaudeAgentBackend│      │ AnthropicAPIBackend│
       │   (Agent SDK)     │      │   (Direct API)    │
       └───────┬──────────┘      └───────┬──────────┘
               │                          │
               └──────────┬───────────────┘
                          ▼
                    ┌──────────┐
                    │  Vanna   │
                    └──────────┘
```

## Configuration

### Environment Variables

Add to your `.env` file:

```bash
# LLM Backend Selection
# Options: "claude_agent_sdk" (default) or "anthropic_api"
LLM_BACKEND=claude_agent_sdk

# API Key (required for both backends)
ANTHROPIC_API_KEY=your_api_key_here

# Model Configuration
LLM_MODEL=claude-3-5-sonnet-20241022
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=2048
```

### Switching Backends

**Method 1: Environment Variable**
```bash
# Use Claude Agent SDK (default)
export LLM_BACKEND=claude_agent_sdk
python app.py

# Use Anthropic API
export LLM_BACKEND=anthropic_api
python app.py
```

**Method 2: .env File**
```bash
# Edit .env file
LLM_BACKEND=anthropic_api

# Restart application
python app.py
```

## Backend Comparison

| Feature | Claude Agent SDK | Anthropic API |
|---------|------------------|---------------|
| **Use Case** | Advanced agents | Simple queries |
| **Latency** | Slightly higher | Lower |
| **Features** | Tool use, caching* | Basic completion |
| **Complexity** | More complex | Simpler |
| **Best For** | Multi-step reasoning | Direct SQL generation |

\* Future enhancements

## Code Examples

### Using Claude Agent SDK

```python
from backend.llm.factory import create_llm_backend

# Create backend
backend = create_llm_backend(
    backend_type="claude_agent_sdk",
    config={
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.1,
        "max_tokens": 2048
    }
)

# Submit prompt
response = backend.submit_prompt([
    {"role": "system", "content": "You are a SQL expert."},
    {"role": "user", "content": "Generate SQL for: total customers"}
])

print(f"Backend: {backend.get_backend_name()}")
print(f"Response: {response}")
```

### Using Anthropic API

```python
from backend.llm.factory import create_llm_backend

# Create backend
backend = create_llm_backend(
    backend_type="anthropic_api",
    config={
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.1,
        "max_tokens": 2048
    }
)

# Submit prompt
response = backend.submit_prompt([
    {"role": "system", "content": "You are a SQL expert."},
    {"role": "user", "content": "Generate SQL for: total customers"}
])

print(f"Backend: {backend.get_backend_name()}")
print(f"Response: {response}")
```

### Automatic Fallback

```python
from backend.llm.factory import create_llm_backend

# Try Claude Agent SDK, fallback to Anthropic API if unavailable
try:
    backend = create_llm_backend(backend_type="claude_agent_sdk")
except ValueError:
    backend = create_llm_backend(backend_type="anthropic_api")

print(f"Using backend: {backend.get_backend_name()}")
```

## Testing

### Run All Tests

```bash
# Activate virtual environment
source .venv/Scripts/activate  # Windows Git Bash

# Run backend switching tests
pytest tests/api/test_backend_switching.py -v

# Run API endpoint tests
pytest tests/api/test_api_endpoints.py -v
```

### Test Specific Backend

```bash
# Test Claude Agent SDK
LLM_BACKEND=claude_agent_sdk pytest tests/api/test_backend_switching.py -v

# Test Anthropic API
LLM_BACKEND=anthropic_api pytest tests/api/test_backend_switching.py -v
```

## API Health Check

The `/api/v0/health` endpoint shows which backend is currently active:

```bash
curl http://localhost:5000/api/v0/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "backend": "claude_agent_sdk",
  "database": "connected"
}
```

## Future Enhancements

### Claude Agent SDK Enhancements

1. **Tool/Function Calling**
   ```python
   backend.add_tool_support([
       {
           "name": "get_schema",
           "description": "Get database schema",
           "parameters": {...}
       }
   ])
   ```

2. **Prompt Caching**
   ```python
   backend.enable_caching()
   ```

3. **Multi-Agent Orchestration**
   ```python
   backend.enable_multi_agent(
       planner_agent=True,
       executor_agent=True
   )
   ```

## Troubleshooting

### Backend Not Available

**Problem**: `No LLM backend available` error

**Solution**:
1. Check `ANTHROPIC_API_KEY` is set in `.env`
2. Verify API key is valid
3. Check internet connectivity

### Wrong Backend Used

**Problem**: Application using wrong backend

**Solution**:
1. Check `LLM_BACKEND` in `.env`
2. Restart application after changing
3. Check logs for backend initialization message

### Import Errors

**Problem**: `ModuleNotFoundError` for backend modules

**Solution**:
1. Ensure all files in `backend/llm/` directory
2. Check `__init__.py` files exist
3. Verify PYTHONPATH includes project root

## Best Practices

1. **Development**: Use Claude Agent SDK for full features
2. **Production**: Use Anthropic API for stability and lower latency
3. **Testing**: Test both backends before deployment
4. **Monitoring**: Log backend name with each request
5. **Fallback**: Configure automatic fallback in production

## Performance Comparison

| Metric | Claude Agent SDK | Anthropic API |
|--------|------------------|---------------|
| Avg Response Time | ~2-3s | ~1-2s |
| Cold Start | ~5s | ~3s |
| Memory Usage | Higher | Lower |
| Token Efficiency | Better (caching*) | Standard |

\* When caching enabled (future)

## Support

For issues with:
- **Backend switching**: Check this guide
- **API errors**: Check logs in `detomo_sql_ai.log`
- **Configuration**: Verify `.env` file
- **General help**: See main [README.md](README.md)

---

**Last Updated**: 2025-10-26
**Version**: 1.0.0
