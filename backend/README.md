# Detomo SQL AI - Backend

FastAPI backend with Vanna AI and Claude Agent SDK for natural language to SQL conversion.

## 🚀 Quick Start

### Local Development

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run training (first time only)
python scripts/train_chinook.py

# Start server
python claude_agent_server.py
```

Server will be available at: http://localhost:8000

### Docker Development

```bash
# From project root
docker-compose up backend
```

## 📚 API Documentation

Interactive API docs available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

For detailed API documentation, see: `../docs/API_DOCUMENTATION.md`

## 🧪 Testing

```bash
# Run all tests
PYTHONPATH=. pytest

# Run with coverage
PYTHONPATH=. pytest --cov=src --cov-report=html

# Run specific test suite
PYTHONPATH=. pytest tests/unit/
PYTHONPATH=. pytest tests/integration/

# View coverage report
open htmlcov/index.html  # macOS
```

## 📁 Project Structure

```
backend/
├── claude_agent_server.py   # Main FastAPI application
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not committed)
├── .env.example             # Environment template
├── Dockerfile.dev           # Development Docker image
│
├── src/                     # Source code
│   ├── detomo_vanna.py     # Vanna AI integration with Claude
│   └── cache.py            # In-memory cache for query state
│
├── tests/                   # All tests
│   ├── unit/               # Unit tests (42 tests)
│   │   ├── test_agent_endpoint.py
│   │   ├── test_detomo_vanna.py
│   │   └── test_cache.py
│   └── integration/        # Integration tests (40 tests)
│       ├── test_training.py
│       ├── test_api_core.py
│       └── test_api_extended.py
│
├── scripts/                 # Utility scripts
│   └── train_chinook.py    # Training data loader
│
├── training_data/          # Training examples
│   └── chinook/
│       ├── ddl/            # DDL files (12 files)
│       ├── documentation/  # Table docs (11 files)
│       └── questions/      # Q&A pairs (70 pairs)
│
└── data/                    # Databases
    └── chinook.db          # SQLite sample database
```

## 🔧 Environment Variables

Required environment variables in `.env`:

```env
# Anthropic API
ANTHROPIC_API_KEY=sk-ant-your-api-key-here

# Database
DATABASE_PATH=data/chinook.db
VECTOR_DB_PATH=./detomo_vectordb

# Server configuration
SERVER_HOST=localhost
SERVER_PORT=8000
LOG_LEVEL=info

# Model configuration (optional)
CLAUDE_MODEL=claude-haiku-4-5-20251001
CLAUDE_TEMPERATURE=0.1
CLAUDE_MAX_TOKENS=2048
```

## 🎯 Key Features

- **Natural Language to SQL**: Convert questions to SQL using Vanna AI + Claude
- **RAG-based**: ChromaDB vector store for context retrieval
- **Multi-language**: Supports English and Japanese queries
- **SQL Execution**: Automatic query execution on SQLite database
- **Visualization**: Plotly chart generation from results
- **Training API**: Add/remove training data via REST API
- **Caching**: In-memory cache for query state management
- **High Accuracy**: 100% SQL accuracy on test queries

## 📊 API Endpoints

### Core Endpoints

- `POST /api/v0/query` - All-in-one: NL → SQL → Results → Chart
- `GET /api/v0/health` - Health check with system status
- `POST /api/v0/train` - Add training data

### Extended Endpoints (Vanna-Flask Pattern)

- `GET /api/v0/generate_questions` - Get suggested questions
- `POST /api/v0/generate_sql` - Generate SQL from question
- `POST /api/v0/run_sql` - Execute cached SQL
- `POST /api/v0/generate_plotly_figure` - Generate chart
- `POST /api/v0/generate_followup_questions` - Get follow-up questions
- `POST /api/v0/load_question` - Load cached query state
- `GET /api/v0/get_question_history` - Get query history
- `GET /api/v0/get_training_data` - Get all training data
- `POST /api/v0/remove_training_data` - Remove training item
- `GET /api/v0/download_csv` - Download results as CSV

## 🧬 Technology Stack

- **Framework**: FastAPI 0.120.0
- **LLM**: Claude Sonnet 4.5 (via Anthropic API)
- **RAG**: Vanna AI 0.7.9 + ChromaDB
- **Database**: SQLite (Chinook sample)
- **Testing**: pytest + pytest-cov
- **Validation**: Pydantic 2.12.3

## 📈 Performance Metrics

- **SQL Accuracy**: 100% (20/20 test queries)
- **Response Time**: 4.57s mean, 5.54s p95
- **Test Coverage**: 100% (src/ modules)
- **Total Tests**: 82 tests passing

## 🔗 Related Documentation

- **Architecture**: `../docs/ARCHITECTURE.md`
- **API Reference**: `../docs/API_DOCUMENTATION.md`
- **Deployment Guide**: `../docs/DEPLOYMENT.md`
- **Project Overview**: `../README.md`
- **Task Master**: `../TASK_MASTER.md`

## 🐛 Troubleshooting

### Server won't start

```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill process if needed
kill -9 <PID>
```

### Import errors

```bash
# Make sure PYTHONPATH includes current directory
export PYTHONPATH=.  # Unix
set PYTHONPATH=.     # Windows

# Or run with explicit PYTHONPATH
PYTHONPATH=. python claude_agent_server.py
```

### ChromaDB locked

```bash
# Stop all processes using ChromaDB
# Delete lock file
rm detomo_vectordb/chroma.sqlite3-wal

# Re-run training
python scripts/train_chinook.py
```

### API key error

```bash
# Verify .env file exists and has valid key
cat .env | grep ANTHROPIC_API_KEY

# Key should start with: sk-ant-
```

## 📝 License

Copyright © 2025 Detomo SQL AI Team

---

**Last Updated**: 2025-10-27
