# Detomo SQL AI

**AI-Powered Text-to-SQL Application**

Convert natural language (Japanese/English) to SQL queries with auto-generated visualizations.

[![Version](https://img.shields.io/badge/version-1.0-blue.svg)](https://github.com/detomo/sql-agent)
[![Python](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

## Overview

Detomo SQL AI is an intelligent database query assistant that enables non-technical users to query databases using natural language. Built with Claude Agent SDK and Vanna AI framework, it provides accurate SQL generation and beautiful visualizations.

### Key Features

- 🤖 **AI-Powered**: Uses Claude 3.5 Sonnet for SQL generation with switchable backends (Claude Agent SDK / Anthropic API)
- 🌏 **Bilingual**: Supports Japanese and English queries
- 📊 **Auto Visualization**: Generates charts automatically with Plotly
- 🎯 **High Accuracy**: Target ≥85% SQL correctness
- ⚡ **Fast Response**: < 5 seconds for most queries
- 🔒 **Secure**: Read-only database access, SQL injection prevention

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **LLM Backend** | Claude Agent SDK (default) / Anthropic API (switchable) |
| **RAG Framework** | Vanna AI |
| **Vector Database** | ChromaDB |
| **Embedding Model** | BAAI/bge-m3 (HuggingFace) |
| **Database** | SQLite (Chinook sample database) |
| **Backend** | Python 3.10+, Flask |
| **Visualization** | Plotly |

---

## Quick Start

### Prerequisites

- Python 3.10 or higher
- `uv` package manager (recommended) or `pip`
- Anthropic API key

### Installation

```bash
# 1. Clone repository
git clone https://github.com/detomo/sql-agent.git
cd sql-agent

# 2. Create virtual environment
uv venv
source .venv/Scripts/activate  # Windows Git Bash
# or
.venv\Scripts\Activate.ps1     # Windows PowerShell

# 3. Install dependencies
uv pip install -r requirements.txt

# 4. Setup environment variables
# Edit .env and add your Anthropic API key
ANTHROPIC_API_KEY=your_key_here

# 5. Verify database
python scripts/verify_db.py

# 6. Train the model (first time only)
python scripts/train_chinook.py

# 7. Run the application
python app.py
```

Visit http://localhost:5000 to use the application.

**Quick Start Guide**: See [docs/guides/QUICKSTART_API.md](docs/guides/QUICKSTART_API.md) for detailed 5-minute setup.

---

## Project Structure

```
SQL-Agent/
├── README.md                    # This file - Project overview
├── TASK_MASTER.md               # Project progress tracker
├── CLAUDE.md                    # Instructions for Claude Code Assistant
├── PRD.md                       # Product Requirements Document
│
├── app.py                       # Main Flask application
├── run_tests.py                 # Test runner script
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (not in git)
│
├── api/                         # API layer
│   ├── routes.py                # 8 RESTful API endpoints
│   └── errors.py                # Error handling middleware
│
├── backend/                     # Backend abstraction layer
│   └── llm/                     # LLM backend implementations
│       ├── base.py              # Abstract base class
│       ├── claude_agent_backend.py   # Claude Agent SDK backend
│       ├── anthropic_api_backend.py  # Anthropic API backend
│       └── factory.py           # Backend factory with auto-detection
│
├── data/                        # Database files
│   └── chinook.db               # SQLite sample database (884KB)
│
├── docs/                        # All documentation
│   ├── README.md                # Documentation index
│   ├── api/                     # API documentation
│   │   ├── API_DOCUMENTATION.md      # Complete API reference
│   │   └── BACKEND_SWITCHING.md      # Backend switching guide
│   ├── guides/                  # User guides
│   │   └── QUICKSTART_API.md         # 5-minute quick start
│   └── development/             # Development documentation
│       ├── TASK_05_SUMMARY.md        # Task completion summaries
│       ├── PROJECT_STRUCTURE.md      # Detailed structure guide
│       └── REORGANIZATION_SUMMARY.md # Structure reorganization log
│
├── scripts/                     # Utility scripts
│   ├── train_chinook.py         # Load training data into vector DB
│   ├── reset_training.py        # Reset vector database
│   ├── check_training.py        # Show training statistics
│   └── verify_db.py             # Verify database integrity
│
├── src/                         # Source code
│   ├── config.py                # Configuration management
│   ├── detomo_vanna_dev.py      # Development Vanna class
│   ├── detomo_vanna_prod.py     # Production Vanna class
│   └── claude_agent_wrapper.py  # Claude Agent wrapper (legacy)
│
├── tasks/                       # Task definition files
│   ├── TASK_01_setup_chinook_database.md
│   ├── TASK_02_create_training_data.md
│   └── ... (12 tasks total)
│
├── tests/                       # Test suite
│   ├── README.md                # Testing documentation
│   ├── unit/                    # Unit tests (individual components)
│   │   └── test_detomo_vanna.py
│   └── integration/             # Integration tests (components together)
│       ├── test_api_endpoints.py
│       ├── test_backend_switching.py
│       └── test_app_structure.py
│
├── training_data/               # Training data for Vanna AI
│   └── chinook/
│       ├── ddl/                 # Database schema (12 files)
│       ├── documentation/       # Table documentation (11 files)
│       └── questions/           # Q&A pairs (70 pairs in 4 JSON files)
│
├── static/                      # Frontend static assets (future)
└── templates/                   # HTML templates (future)
```

### Key Directories

- **`api/`** - Flask API routes and error handling
- **`backend/`** - LLM backend abstraction layer (Claude Agent SDK / Anthropic API)
- **`docs/`** - All project documentation (API, guides, development)
- **`scripts/`** - Utility scripts for training, verification, maintenance
- **`src/`** - Core application logic and Vanna integration
- **`tests/`** - Test suite (unit + integration tests)
- **`training_data/`** - Training data for SQL generation (DDL, docs, Q&A)

---

## Quick Links

### 🚀 Getting Started
- [Quick Start (5 min)](docs/guides/QUICKSTART_API.md)
- [CLAUDE.md](CLAUDE.md) - Instructions for Claude Code Assistant

### 📚 Documentation
- [API Documentation](docs/api/API_DOCUMENTATION.md) - Complete API reference
- [Backend Switching](docs/api/BACKEND_SWITCHING.md) - Switch between LLM backends
- [All Documentation](docs/README.md) - Documentation index

### 📊 Project Management
- [TASK_MASTER.md](TASK_MASTER.md) - Project progress tracker
- [PRD.md](PRD.md) - Product requirements
- [Tasks](tasks/) - Individual task files

### 🧪 Testing
- [Testing Guide](tests/README.md) - How to run tests
- `python run_tests.py` - Run all tests
- `python run_tests.py unit` - Unit tests only
- `python run_tests.py integration` - Integration tests only

---

## Development Status

**Version**: 1.0.0
**Status**: In Development (42% complete)
**Start Date**: 2025-10-25
**Target Completion**: 8 weeks

### Progress by Phase

| Phase | Tasks | Status | Progress |
|-------|-------|--------|----------|
| Phase 1: Foundation | Tasks 01-04 | ✅ Completed | 100% |
| Phase 2: API Development | Task 05 | ✅ Completed | 100% |
| Phase 3: Frontend | Task 06 | ⏸️ Not Started | 0% |
| Phase 4: Testing & Optimization | Tasks 07-10 | ⏸️ Not Started | 0% |
| Phase 5: Deployment | Task 11 | ⏸️ Not Started | 0% |
| Phase 6: Polish & Launch | Task 12 | ⏸️ Not Started | 0% |

**Overall Progress**: [████████░░░░░░░░░░░░] 42% (5/12 tasks completed)

### Completed Features
- ✅ SQLite Chinook database setup and verification
- ✅ Training data created (93 items: 12 DDL, 11 docs, 70 Q&A pairs)
- ✅ DetomoVanna class with SQLite support
- ✅ Training scripts and vector database
- ✅ Flask API with 8 endpoints
- ✅ Backend abstraction layer (Claude Agent SDK / Anthropic API)
- ✅ Comprehensive testing (26 tests)
- ✅ Complete documentation

### Next Steps
- Task 06: UI Customization
- Task 07: Testing & QA
- Task 08-12: Optimization, deployment, and launch

---

## Running Tests

```bash
# Run all tests
python run_tests.py

# Run unit tests only
python run_tests.py unit

# Run integration tests only
python run_tests.py integration

# Run with verbose output
python run_tests.py -v

# Or use pytest directly
pytest tests/ -v
pytest tests/unit/ -v
pytest tests/integration/ -v
```

See [tests/README.md](tests/README.md) for detailed testing documentation.

---

## API Endpoints

The Flask API provides 8 RESTful endpoints:

1. `GET /api/v0/health` - Health check with backend info
2. `POST /api/v0/generate_sql` - Generate SQL from natural language
3. `POST /api/v0/run_sql` - Execute SQL query
4. `POST /api/v0/ask` - Complete workflow (question → SQL → results)
5. `POST /api/v0/generate_plotly_figure` - Generate visualization
6. `GET /api/v0/get_training_data` - Get training data statistics
7. `POST /api/v0/train` - Add new training data
8. `DELETE /api/v0/remove_training_data` - Remove training data

See [docs/api/API_DOCUMENTATION.md](docs/api/API_DOCUMENTATION.md) for complete API reference.

---

## File Organization Rules

### Root Directory (Only 3 Files)
- `README.md` - Project overview (this file)
- `TASK_MASTER.md` - Project progress tracker
- `CLAUDE.md` - Instructions for Claude Code Assistant

### All Other Documentation → `docs/`
- API documentation → `docs/api/`
- User guides → `docs/guides/`
- Development docs → `docs/development/`

### Scripts → `scripts/`
- Training scripts
- Verification scripts
- Utility scripts

### Tests → `tests/`
- Unit tests → `tests/unit/`
- Integration tests → `tests/integration/`

**See [CLAUDE.md](CLAUDE.md) for detailed file organization guidelines.**

---

## License

This project is licensed under the MIT License.

---

## Support

- **Quick Start**: [docs/guides/QUICKSTART_API.md](docs/guides/QUICKSTART_API.md)
- **Documentation**: [docs/README.md](docs/README.md)
- **Issues**: GitHub Issues
- **Email**: support@detomo.com

---

**Last Updated**: 2025-10-26
