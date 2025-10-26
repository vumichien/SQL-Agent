# Quick Start Guide - Detomo SQL AI API

Get the API running in 5 minutes!

---

## Prerequisites

- Python 3.10+
- `uv` package manager (or pip)
- Anthropic API key

---

## Step 1: Clone & Setup (1 minute)

```bash
# Navigate to project
cd c:/Project/Detomo/2025/SQL-Agent

# Create virtual environment
uv venv

# Activate virtual environment (Windows Git Bash)
source .venv/Scripts/activate

# Or on Windows PowerShell
.venv\Scripts\Activate.ps1

# Install dependencies
uv pip install -r requirements.txt
```

---

## Step 2: Configure API Key (1 minute)

Edit `.env` file:

```bash
# LLM Configuration
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Backend Selection (optional - defaults to claude_agent_sdk)
LLM_BACKEND=claude_agent_sdk
```

**Get API Key**: https://console.anthropic.com/

---

## Step 3: Verify Setup (1 minute)

```bash
# Test structure
python test_app_structure.py
```

Expected output:
```
✓ All imports successful
✓ Backend detection working
✓ Error handlers registered
✓ API blueprint registered
✓ Found 9 routes
```

---

## Step 4: Start Server (30 seconds)

```bash
python app.py
```

Expected output:
```
================================================================================
DETOMO SQL AI - Starting Application
================================================================================
Available backends: ['claude_agent_sdk', 'anthropic_api']
✓ LLM Backend initialized: claude_agent_sdk
✓ Vanna initialized successfully
✓ Training data loaded: 93 items
================================================================================
Application initialized successfully!
Backend: claude_agent_sdk
Database: data/chinook.db
Vector DB: ./detomo_vectordb
================================================================================
 * Running on http://0.0.0.0:5000
```

---

## Step 5: Test API (1 minute)

### Open new terminal and test:

```bash
# 1. Health check
curl http://localhost:5000/api/v0/health

# 2. Ask a question
curl -X POST http://localhost:5000/api/v0/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How many customers are there?"}'

# 3. Ask in Japanese
curl -X POST http://localhost:5000/api/v0/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "顧客は何人いますか？"}'
```

---

## Quick Test Examples

### Example 1: Generate SQL Only

```bash
curl -X POST http://localhost:5000/api/v0/generate_sql \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the top 5 albums by number of tracks?"}'
```

Response:
```json
{
  "question": "What are the top 5 albums by number of tracks?",
  "sql": "SELECT a.Title, COUNT(t.TrackId) as track_count FROM albums a JOIN tracks t ON a.AlbumId = t.AlbumId GROUP BY a.AlbumId ORDER BY track_count DESC LIMIT 5",
  "status": "success"
}
```

### Example 2: Complete Workflow

```bash
curl -X POST http://localhost:5000/api/v0/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Show me the top 3 genres by number of tracks"}'
```

Response:
```json
{
  "question": "Show me the top 3 genres by number of tracks",
  "sql": "SELECT g.Name, COUNT(t.TrackId) as track_count FROM genres g JOIN tracks t ON g.GenreId = t.GenreId GROUP BY g.GenreId ORDER BY track_count DESC LIMIT 3",
  "data": [
    {"Name": "Rock", "track_count": 1297},
    {"Name": "Latin", "track_count": 579},
    {"Name": "Metal", "track_count": 374}
  ],
  "columns": ["Name", "track_count"],
  "row_count": 3,
  "status": "success"
}
```

### Example 3: Training Data Stats

```bash
curl http://localhost:5000/api/v0/get_training_data
```

Response:
```json
{
  "ddl_count": 12,
  "documentation_count": 11,
  "sql_count": 70,
  "total": 93,
  "status": "success"
}
```

---

## Switch Backend

### Use Anthropic API Instead

```bash
# Stop server (Ctrl+C)

# Edit .env
LLM_BACKEND=anthropic_api

# Restart server
python app.py
```

Check backend:
```bash
curl http://localhost:5000/api/v0/health | jq .backend
# Returns: "anthropic_api"
```

---

## Run Tests

```bash
# Run all tests
pytest tests/api/ -v

# Run specific tests
pytest tests/api/test_backend_switching.py -v
pytest tests/api/test_api_endpoints.py -v
```

---

## Common Issues

### Issue: "No LLM backend available"
**Solution**: Set `ANTHROPIC_API_KEY` in `.env` file

### Issue: "ModuleNotFoundError"
**Solution**: Run `uv pip install -r requirements.txt`

### Issue: Port 5000 already in use
**Solution**: Change port in `app.py` or kill process on port 5000

### Issue: Japanese characters not displaying
**Solution**: Ensure terminal supports UTF-8 encoding

---

## API Documentation

Full documentation: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

Key endpoints:
- `/api/v0/health` - Health check
- `/api/v0/generate_sql` - Generate SQL
- `/api/v0/run_sql` - Execute SQL
- `/api/v0/ask` - Complete workflow
- `/api/v0/get_training_data` - Training stats

---

## Backend Switching

Full guide: [BACKEND_SWITCHING.md](BACKEND_SWITCHING.md)

Quick switch:
```bash
# Claude Agent SDK (default)
export LLM_BACKEND=claude_agent_sdk

# Anthropic API
export LLM_BACKEND=anthropic_api
```

---

## Next Steps

1. ✅ API is running!
2. Read [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for all endpoints
3. Read [BACKEND_SWITCHING.md](BACKEND_SWITCHING.md) for backend options
4. Try the example queries above
5. Build your frontend (Task 06)

---

## Development Mode

### Enable debug mode:

Edit `.env`:
```
FLASK_DEBUG=True
LOG_LEVEL=DEBUG
```

This enables:
- Auto-reload on code changes
- Detailed error messages
- Debug logging

---

## Production Considerations

Before production:
1. Set `FLASK_DEBUG=False`
2. Set `LOG_LEVEL=WARNING`
3. Add authentication
4. Configure CORS properly
5. Add rate limiting
6. Use production WSGI server (gunicorn)

---

## Support

- API Documentation: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- Backend Guide: [BACKEND_SWITCHING.md](BACKEND_SWITCHING.md)
- Task Summary: [TASK_05_SUMMARY.md](TASK_05_SUMMARY.md)
- Main README: [README.md](README.md)

---

**That's it! Your API is running!** 🎉

Try asking questions in both English and Japanese, and watch the AI generate accurate SQL queries for the Chinook database.
