# Project Structure - Detomo SQL AI

Detailed overview of the project directory structure.

---

## Directory Tree

```
SQL-Agent/
├── api/                              # API routes and error handling
│   ├── __init__.py
│   ├── routes.py                     # 8 API endpoint handlers
│   └── errors.py                     # Error handling middleware
│
├── backend/                          # Backend abstraction layer
│   ├── __init__.py
│   └── llm/                          # LLM backend implementations
│       ├── __init__.py
│       ├── base.py                   # Abstract base class
│       ├── claude_agent_backend.py   # Claude Agent SDK
│       ├── anthropic_api_backend.py  # Anthropic API
│       └── factory.py                # Backend factory
│
├── data/                             # Database files
│   └── chinook.db                    # SQLite database (884KB)
│
├── docs/                             # Documentation
│   ├── README.md                     # Documentation index
│   ├── api/                          # API documentation
│   │   ├── API_DOCUMENTATION.md      # Complete API reference
│   │   └── BACKEND_SWITCHING.md      # Backend switching guide
│   ├── guides/                       # User guides
│   │   └── QUICKSTART_API.md         # 5-minute quick start
│   └── development/                  # Development docs
│       ├── CLAUDE.md                 # Claude Code Assistant instructions
│       └── TASK_05_SUMMARY.md        # Task completion summary
│
├── scripts/                          # Utility scripts
│   ├── __init__.py
│   ├── train_chinook.py              # Training data loader
│   ├── reset_training.py             # Reset vector database
│   └── check_training.py             # Check training stats
│
├── src/                              # Source code
│   ├── __init__.py
│   ├── config.py                     # Configuration management
│   ├── detomo_vanna_dev.py          # Development Vanna class
│   ├── detomo_vanna_prod.py         # Production Vanna class
│   └── claude_agent_wrapper.py       # Claude Agent wrapper
│
├── static/                           # Static files (future)
│   └── (Frontend assets will go here)
│
├── templates/                        # HTML templates (future)
│   └── (Frontend templates will go here)
│
├── tests/                            # Test suite
│   ├── README.md                     # Testing documentation
│   ├── __init__.py
│   ├── unit/                         # Unit tests
│   │   ├── __init__.py
│   │   └── test_detomo_vanna.py     # Vanna class tests
│   └── integration/                  # Integration tests
│       ├── __init__.py
│       ├── test_api_endpoints.py     # API endpoint tests
│       ├── test_backend_switching.py # Backend switching tests
│       └── test_app_structure.py     # App structure tests
│
├── training_data/                    # Training data files
│   └── chinook/
│       ├── ddl/                      # DDL files (12 files)
│       ├── documentation/            # Documentation (11 files)
│       └── questions/                # Q&A pairs (4 JSON files, 70 pairs)
│
├── app.py                            # Main Flask application
├── run_tests.py                      # Test runner script
├── requirements.txt                  # Python dependencies
├── setup.py                          # Package setup (future)
├── .env                              # Environment variables (not in git)
├── .gitignore                        # Git ignore rules
├── README.md                         # Project README
├── PRD.md                            # Product Requirements Document
├── TASK_MASTER.md                    # Project progress tracker
└── PROJECT_STRUCTURE.md              # This file
```

---

## Directory Descriptions

### `/api` - API Layer
Flask API routes and error handling.

**Files:**
- `routes.py` - 8 RESTful API endpoints
- `errors.py` - Custom error classes and handlers

**Purpose:**
- Handle HTTP requests/responses
- Validate input
- Return JSON responses
- Handle errors gracefully

### `/backend` - Backend Abstraction
LLM backend abstraction layer for easy switching.

**Files:**
- `llm/base.py` - Abstract base class
- `llm/claude_agent_backend.py` - Claude Agent SDK implementation
- `llm/anthropic_api_backend.py` - Anthropic API implementation
- `llm/factory.py` - Backend factory with auto-detection

**Purpose:**
- Abstract LLM backend details
- Enable backend switching
- Provide common interface
- Support future backends

### `/data` - Database
SQLite database files.

**Files:**
- `chinook.db` - Sample music database (11 tables, 15K+ rows)

**Purpose:**
- Store sample data for demos
- Provide realistic test environment

### `/docs` - Documentation
All project documentation organized by category.

**Structure:**
- `api/` - API documentation
- `guides/` - User guides
- `development/` - Development docs

**Purpose:**
- Centralize documentation
- Easy navigation
- Version control
- Keep project root clean

### `/scripts` - Utility Scripts
Helper scripts for training and maintenance.

**Files:**
- `train_chinook.py` - Load training data into vector DB
- `reset_training.py` - Reset vector database
- `check_training.py` - Show training statistics

**Purpose:**
- Automate common tasks
- Maintain training data
- Database management

### `/src` - Source Code
Core application logic.

**Files:**
- `config.py` - Configuration management
- `detomo_vanna_dev.py` - Development Vanna class
- `detomo_vanna_prod.py` - Production Vanna class
- `claude_agent_wrapper.py` - LLM wrapper

**Purpose:**
- Core business logic
- Vanna integration
- Configuration management

### `/tests` - Test Suite
Comprehensive test coverage.

**Structure:**
- `unit/` - Unit tests (individual components)
- `integration/` - Integration tests (components working together)

**Purpose:**
- Ensure code quality
- Prevent regressions
- Document expected behavior
- Enable refactoring

### `/training_data` - Training Data
Vector database training data.

**Structure:**
- `ddl/` - Database schema definitions
- `documentation/` - Table and business rule docs
- `questions/` - Q&A pairs for SQL generation

**Purpose:**
- Train Vanna AI
- Improve SQL generation accuracy
- Document database schema

---

## Key Files

### Root Level

**app.py**
- Main Flask application
- Initializes backends
- Registers routes
- Entry point for API server

**run_tests.py**
- Test runner script
- Simplifies test execution
- Supports filtering (unit/integration)

**requirements.txt**
- Python dependencies
- Install with: `uv pip install -r requirements.txt`

**.env**
- Environment variables
- API keys
- Configuration
- NOT in git (use .env.example as template)

**.gitignore**
- Git ignore rules
- Excludes virtual env, logs, cache
- Protects sensitive files

**README.md**
- Project overview
- Quick start guide
- Key features
- Installation instructions

**TASK_MASTER.md**
- Project progress tracker
- Task status
- Phase management
- Timeline

**PRD.md**
- Product Requirements Document
- Feature specifications
- Success criteria

---

## File Counts

### Code Files
- Python files: ~25 files
- Total lines of code: ~5,000 lines

### Test Files
- Test files: 4 files
- Total tests: 26 tests

### Documentation
- Markdown files: ~15 files
- Total documentation: ~3,500 lines

### Training Data
- DDL files: 12 files
- Documentation: 11 files
- Q&A JSON: 4 files (70 pairs)

---

## Import Paths

### Standard Imports
```python
# Import from src/
from src.config import config
from src.detomo_vanna_dev import create_vanna_dev

# Import from backend/
from backend.llm.factory import create_llm_backend

# Import from api/
from api.routes import api_bp
from api.errors import APIError
```

### Test Imports
```python
# Add project root to path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Then import normally
from src.config import config
```

---

## Navigation Tips

### Find by Task
- **Setup project**: README.md, docs/guides/QUICKSTART_API.md
- **Use API**: docs/api/API_DOCUMENTATION.md
- **Switch backends**: docs/api/BACKEND_SWITCHING.md
- **Run tests**: tests/README.md, run_tests.py
- **Add training data**: scripts/train_chinook.py
- **Check progress**: TASK_MASTER.md

### Find by Role
- **User**: README.md, docs/guides/
- **Developer**: docs/development/, src/, backend/, api/
- **Tester**: tests/, run_tests.py
- **AI Assistant**: docs/development/CLAUDE.md
- **Project Manager**: TASK_MASTER.md, PRD.md

---

## Git Structure

### Tracked Files
- All source code
- Documentation
- Training data
- Requirements
- Configuration templates

### Ignored Files
- `.venv/` - Virtual environment
- `*.log` - Log files
- `.env` - Environment variables
- `__pycache__/` - Python cache
- `detomo_vectordb/` - Vector database
- `.pytest_cache/` - Test cache

---

## Future Additions

### Planned Directories
- `/frontend` - React/Vue frontend
- `/migrations` - Database migrations
- `/docker` - Docker configuration
- `/deploy` - Deployment scripts

### Planned Files
- `docker-compose.yml` - Docker setup
- `.github/workflows/` - CI/CD
- `CHANGELOG.md` - Version history
- `CONTRIBUTING.md` - Contribution guide

---

## Maintenance

### Keep Updated
- Update this file when structure changes
- Document new directories
- Explain new file purposes
- Keep counts accurate

### Review Schedule
- Monthly: Review structure
- Per release: Update documentation
- Major changes: Update immediately

---

**Last Updated**: 2025-10-26
**Version**: 1.0
