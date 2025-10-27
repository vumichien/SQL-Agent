# CLAUDE.md - Guide for Claude Code Agent

**Project**: Detomo SQL AI v3.0 (Monorepo Structure)
**Last Updated**: 2025-10-27

---

## OVERVIEW

This guide helps Claude Code agent (or any developer) implement the Detomo SQL AI project efficiently. Follow this workflow for each task to ensure consistency and completeness.

---

## START COMMAND

**When the user types "start"**, Claude Code agent should:

### 1. Check Current Task Status

Read [TASK_MASTER.md](TASK_MASTER.md) to:
- Identify completed tasks (✅ Done)
- Identify in-progress tasks (⏳ In Progress)
- Identify blocked tasks (dependencies not met)
- Calculate overall progress (X/12 tasks completed)

### 2. Verify Environment & Prerequisites

Check that everything is set up correctly:

```bash
# Verify virtual environment
python --version  # Should be 3.10+

# Check if required files exist
ls TASK_MASTER.md CLAUDE.md tasks/ docs/PRD.md

# Check git status (if applicable)
git status

# Verify dependencies (backend)
cd backend && uv pip list | grep -E "vanna|fastapi|anthropic" && cd ..
```

### 3. Find Next Task

Based on TASK_MASTER.md:
- Identify the next task to work on (first "Not Started" task with dependencies met)
- Check task dependencies are satisfied
- Read the task file: `tasks/TASK_XX_name.md`

### 4. Display Status Summary

Present a clear summary:

```
========================================
DETOMO SQL AI - PROJECT STATUS
========================================

Overall Progress: X/12 tasks completed (Y%)

Phase 1: Core Backend Setup
  ✅ TASK 01: Claude Agent Endpoint Server - DONE
  ⬜ TASK 02: Vanna Custom Class - NOT STARTED

Phase 2: Training Data & Knowledge Base
  ⬜ TASK 03: Training Data Preparation - NOT STARTED
  ⬜ TASK 04: Training Script - NOT STARTED

... (continue for all phases)

========================================
NEXT TASK: TASK_02 (Vanna Custom Class)
========================================

Dependencies:
  ✅ TASK 01 (Claude Agent Endpoint) - COMPLETED

Estimated Time: 6-8 hours

Objectives:
1. Create src/detomo_vanna.py module
2. Implement ClaudeAgentChat class
3. Implement DetomoVanna class
4. Write unit tests

Task File: tasks/TASK_02_vanna_custom_class.md

========================================
```

### 5. Ask for Confirmation

Ask the user:

```
Ready to start TASK_02: Vanna Custom Class Implementation?

This task will:
- Create src/detomo_vanna.py with custom Vanna classes
- Implement integration with Claude Agent SDK
- Write unit tests

Prerequisites check:
✅ TASK_01 completed (Claude Agent endpoint available)
✅ Virtual environment active
⚠️  Claude Agent endpoint should be running on http://localhost:8000

Do you want to proceed? (yes/no)
```

### 6. Start Implementation (if confirmed)

If user confirms:
1. Read the task file in detail
2. Create necessary folder structure
3. Begin implementation following the task steps
4. Update progress in real-time

---

## ENVIRONMENT SETUP

### Prerequisites

1. **Python Version**: Python 3.10 or higher
2. **Virtual Environment**: Create in `/backend` directory
3. **Package Manager**: Use `uv pip install` for all package installations
4. **Docker**: Optional, for containerized development

### Initial Setup Steps

```bash
# Navigate to backend directory
cd backend

# 1. Activate virtual environment
# On Windows:
.venv\Scripts\activate

# On Unix/macOS:
source .venv/bin/activate

# 2. Verify Python version
python --version
# Should output: Python 3.10.x or higher

# 3. Install dependencies
uv pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Environment Variables

Create a `.env` file in the `/backend` directory:

```bash
# Anthropic API (for Claude Agent SDK server)
ANTHROPIC_API_KEY=sk-ant-your-api-key-here

# Claude Agent SDK endpoint
CLAUDE_AGENT_ENDPOINT=http://localhost:8000/generate

# Database
DATABASE_PATH=data/chinook.db

# Vector Database (managed by Vanna)
VECTOR_DB_PATH=./detomo_vectordb
```

### Docker Development (Alternative)

```bash
# From project root
docker-compose up backend

# Backend will be available at http://localhost:8000
```

---

## WORKFLOW CHECKLIST

When implementing each task, follow this checklist:

### Step 1: Read Task File
- [ ] Open the task file from `tasks/TASK_XX_name.md`
- [ ] Read **Overview**, **Objectives**, and **Requirements** sections
- [ ] Understand **Dependencies** - make sure prerequisite tasks are completed
- [ ] Review **Success Criteria** to know what "done" looks like

### Step 2: Plan Implementation
- [ ] Review **Implementation Steps** in the task file
- [ ] Check **File Structure** to understand what files to create/modify
- [ ] Identify any new dependencies to add to `requirements.txt`
- [ ] Consider edge cases and error handling

### Step 3: Implement Code
- [ ] Create/modify files according to task requirements
- [ ] Follow Python best practices (PEP 8, type hints, docstrings)
- [ ] Add comprehensive error handling
- [ ] Add logging where appropriate
- [ ] Write clear comments for complex logic

### Step 4: Write Tests
- [ ] Create unit tests in `tests/unit/` for isolated components
- [ ] Create integration tests in `tests/integration/` for multi-component flows
- [ ] Aim for ≥80% code coverage
- [ ] Test both happy paths and error cases

### Step 5: Run Tests
```bash
# Navigate to backend (if not already there)
cd backend

# Run all tests
PYTHONPATH=. pytest

# Run with coverage report
PYTHONPATH=. pytest --cov=src --cov=. --cov-report=html

# Run specific test file
PYTHONPATH=. pytest tests/unit/test_specific.py

# Run with verbose output
PYTHONPATH=. pytest -v
```

### Step 6: Manual Testing (if applicable)
- [ ] Start required servers (e.g., `cd backend && python claude_agent_server.py`)
- [ ] Test endpoints with curl/Postman
- [ ] Verify output matches expected behavior
- [ ] Check logs for errors

### Step 7: Update Documentation
- [ ] Update docstrings in code
- [ ] Update `TASK_MASTER.md` - mark task as completed
- [ ] Update `README.md` if new features added
- [ ] Add notes to task file about implementation decisions

### Step 8: Check Context Usage
- [ ] Monitor token/context usage
- [ ] If context < 20% remaining → **Create new chat session**
- [ ] Before switching: Save all progress, update TASK_MASTER.md
- [ ] In new session: Reference TASK_MASTER.md to continue

---

## COMMON COMMANDS

### Development

```bash
# Navigate to backend
cd backend

# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix/macOS

# Install new package
uv pip install package-name

# Update requirements.txt after installing packages
uv pip freeze > requirements.txt

# Run Python script
python script_name.py

# Run script with environment variables from .env
python -c "from dotenv import load_dotenv; load_dotenv()" && python script.py
```

### Testing

```bash
# Navigate to backend (if not already there)
cd backend

# Run all tests
PYTHONPATH=. pytest

# Run with coverage
PYTHONPATH=. pytest --cov=src --cov=. --cov-report=html

# Run specific test file
PYTHONPATH=. pytest tests/unit/test_cache.py

# Run specific test function
PYTHONPATH=. pytest tests/unit/test_cache.py::test_cache_set

# Run with verbose output
PYTHONPATH=. pytest -v

# Run with print statements visible
PYTHONPATH=. pytest -s

# View coverage report
# Open htmlcov/index.html in browser
```

### Running Servers

```bash
# Option 1: Local Development
cd backend
python claude_agent_server.py
# Server runs on http://localhost:8000

# Option 2: Docker
# From project root
docker-compose up backend
# Server runs on http://localhost:8000

# Test API health
curl -X GET http://localhost:8000/api/v0/health

# Test query endpoint
curl -X POST http://localhost:8000/api/v0/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How many customers?"}'
```

### Training & Database

```bash
# Navigate to backend
cd backend

# Run training script
python scripts/train_chinook.py

# Verify ChromaDB data
python -c "from src.detomo_vanna import DetomoVanna; vn = DetomoVanna(config={'path': './detomo_vectordb'}); print(len(vn.get_training_data()))"

# Connect to SQLite database
sqlite3 data/chinook.db
# Inside SQLite:
# .tables          - List all tables
# .schema Customer - Show table schema
# SELECT * FROM Customer LIMIT 5;
# .quit           - Exit
```

---

## TASK EXECUTION ORDER

Follow this order for task implementation (see [TASK_MASTER.md](TASK_MASTER.md) for details):

### Phase 1-6: Backend v2.0 (✅ Completed)
1. **TASK 01**: Claude Agent Endpoint Server ✅
2. **TASK 02**: Vanna Custom Class ✅
3. **TASK 03**: Training Data Preparation ✅
4. **TASK 04**: Training Script ✅
5. **TASK 05**: FastAPI Core Endpoints ✅
6. **TASK 06**: Cache Implementation ✅
7. **TASK 07**: FastAPI Extended Endpoints ✅
8. **TASK 08**: Frontend Setup (Vanilla JS) ✅
9. **TASK 09**: Unit Testing ✅
10. **TASK 10**: Integration Testing ✅
11. **TASK 11**: Optimization & QA ✅
12. **TASK 12**: Documentation ✅

### Phase 7: Frontend Migration (v3.0)
13. **TASK 13**: Project Restructure - Monorepo ✅
14. **TASK 14**: Backend Refactor - Clean Architecture ⏳
15. **TASK 15**: Vue3 + Vite + TypeScript Setup
16. **TASK 16**: Element Plus Integration
17. **TASK 17**: Pinia Store Setup
18. **TASK 18**: Vue Router Setup
19. **TASK 19**: Chat Interface Components
20. **TASK 20**: SQL Display & Results Table
21. **TASK 21**: Plotly Visualization Integration
22. **TASK 22**: Query History Sidebar
23. **TASK 23**: Training Data Management
24. **TASK 24**: Theme & Internationalization
25. **TASK 25**: Authentication System
26. **TASK 26**: Frontend Testing (Vitest)
27. **TASK 27**: E2E Testing (Playwright)
28. **TASK 28**: Docker & Production Deployment

---

## CODE QUALITY STANDARDS

### Python Style
- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Maximum line length: 100 characters
- Use descriptive variable names

### Documentation
- Add docstrings to all functions and classes (Google style)
- Include parameter types, return types, and examples
- Document complex algorithms and business logic

Example:
```python
def generate_sql(self, question: str) -> str:
    """
    Generate SQL query from natural language question.

    Args:
        question (str): Natural language question (English or Japanese)

    Returns:
        str: Generated SQL query

    Raises:
        ValueError: If question is empty
        APIError: If Claude Agent SDK call fails

    Example:
        >>> vn = DetomoVanna(config={...})
        >>> sql = vn.generate_sql("How many customers?")
        >>> print(sql)
        SELECT COUNT(*) FROM Customer
    """
    # Implementation here
```

### Error Handling
- Always validate input parameters
- Use try-except blocks for external calls (API, database, file I/O)
- Log errors with context information
- Return meaningful error messages

Example:
```python
try:
    response = requests.post(self.agent_endpoint, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
except requests.exceptions.Timeout:
    logger.error(f"Timeout calling {self.agent_endpoint}")
    raise APIError("Claude Agent SDK timeout")
except requests.exceptions.RequestException as e:
    logger.error(f"Error calling Claude Agent SDK: {e}")
    raise APIError(f"Failed to call Claude Agent SDK: {str(e)}")
```

### Testing
- Write tests before or alongside implementation (TDD approach)
- Test both happy paths and error cases
- Use fixtures for common test setup
- Mock external dependencies (API calls, database)

---

## TROUBLESHOOTING

### Common Issues

#### Issue 1: Virtual Environment Not Activated
**Symptom**: `command not found: python` or packages not found

**Solution**:
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix/macOS
```

#### Issue 2: Package Installation Fails
**Symptom**: `uv pip install` errors

**Solution**:
```bash
# Update uv
pip install --upgrade uv

# Try installing with pip instead
pip install package-name
```

#### Issue 3: Claude Agent SDK Connection Error
**Symptom**: `Connection refused` when calling `/generate`

**Solution**:
```bash
# Check if server is running
curl http://localhost:8000/health

# If not running, start it
python claude_agent_server.py
```

#### Issue 4: Anthropic API Key Error
**Symptom**: `AuthenticationError: Invalid API key`

**Solution**:
```bash
# Check .env file has correct key
cat .env | grep ANTHROPIC_API_KEY

# Make sure .env is loaded
# Add this to your Python script:
from dotenv import load_dotenv
load_dotenv()
```

#### Issue 5: ChromaDB Lock Error
**Symptom**: `Database is locked` when running training script

**Solution**:
```bash
# Close all processes using ChromaDB
# Delete the lock file
rm detomo_vectordb/chroma.sqlite3-wal

# Re-run training script
python scripts/train_chinook.py
```

#### Issue 6: Import Errors
**Symptom**: `ModuleNotFoundError: No module named 'src'`

**Solution**:
```bash
# Add project root to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Unix/macOS
set PYTHONPATH=%PYTHONPATH%;%cd%  # Windows

# Or use absolute imports
# Instead of: from src.detomo_vanna import ...
# Use: from detomo_vanna import ...
```

---

## CONTEXT MANAGEMENT

### Token Usage Guidelines

Claude Code has a token limit. Monitor usage to avoid hitting limits:

#### When to Create New Chat Session

Create a new chat session when:
- Context usage > 80% (< 20% remaining)
- Switching to a different phase of the project
- After completing 2-3 major tasks

#### Before Switching Sessions

1. **Save all progress**:
   - Commit all code changes (if using git)
   - Update `TASK_MASTER.md` with completion status
   - Add notes to task files about decisions made

2. **Document current state**:
   ```bash
   # Create a session summary
   echo "Session Summary $(date)" >> SESSION_NOTES.md
   echo "- Completed: TASK_01, TASK_02" >> SESSION_NOTES.md
   echo "- Current: TASK_03 (50% done)" >> SESSION_NOTES.md
   echo "- Next: Finish TASK_03, start TASK_04" >> SESSION_NOTES.md
   ```

3. **Verify everything works**:
   - Run all tests: `pytest`
   - Check servers start: `python claude_agent_server.py`
   - Review `TASK_MASTER.md` for accuracy

#### Starting New Session

In the new chat session:
1. Read `TASK_MASTER.md` to understand current progress
2. Read `SESSION_NOTES.md` (if exists) for context
3. Read the current task file to continue work
4. Reference completed task files for implementation patterns

---

## PROJECT STRUCTURE REFERENCE

```
SQL-Agent/                        # Monorepo root
├── CLAUDE.md                     # This file - Claude agent guide
├── TASK_MASTER.md                # Task tracking and progress
├── README.md                     # Project overview and quick start
├── MIGRATION_PLAN_SUMMARY.md     # Phase 7 migration plan
├── docker-compose.yml            # Development containers
├── .gitignore                    # Updated for monorepo
│
├── docs/                         # All documentation
│   ├── PRD.md                    # Product Requirements Document
│   ├── ARCHITECTURE.md           # System architecture
│   ├── API_DOCUMENTATION.md      # API endpoints reference
│   ├── DEPLOYMENT.md             # Deployment guide
│   └── QA_REPORT.md              # Testing & quality report
│
├── tasks/                        # Task files (28 tasks)
│   ├── TASK_01-12_*.md           # Phase 1-6 (Completed)
│   └── TASK_13-28_*.md           # Phase 7 (In Progress)
│
├── backend/                      # FastAPI Backend
│   ├── claude_agent_server.py    # Main FastAPI app
│   ├── requirements.txt          # Python dependencies
│   ├── .env                      # Environment variables (gitignored)
│   ├── .env.example             # Example env file
│   ├── README.md                # Backend documentation
│   ├── Dockerfile.dev           # Development Docker image
│   │
│   ├── src/                     # Source code
│   │   ├── __init__.py
│   │   ├── detomo_vanna.py      # Vanna integration
│   │   └── cache.py             # Cache implementation
│   │
│   ├── tests/                   # All tests (82 tests)
│   │   ├── unit/                # Unit tests (42 tests)
│   │   ├── integration/         # Integration tests (40 tests)
│   │   ├── accuracy/            # SQL accuracy tests
│   │   └── performance/         # Performance benchmarks
│   │
│   ├── scripts/                 # Utility scripts
│   │   └── train_chinook.py     # Training data loader
│   │
│   ├── training_data/           # Training examples (93 items)
│   │   └── chinook/
│   │       ├── ddl/             # DDL files (12)
│   │       ├── documentation/   # Table docs (11)
│   │       └── questions/       # Q&A pairs (70)
│   │
│   ├── data/                    # Databases
│   │   └── chinook.db          # SQLite sample database
│   │
│   └── detomo_vectordb/        # ChromaDB storage (auto-created)
│
├── frontend/                    # Vue3 Frontend (TASK_15+)
│   ├── src/                     # Vue3 source code
│   ├── public/                  # Static assets
│   ├── package.json             # Node dependencies
│   └── vite.config.ts          # Vite configuration
│
├── shared/                      # Shared types/constants
│   └── types/                   # TypeScript types
│
└── static/                      # Legacy Vanilla JS UI (will be replaced)
    ├── index.html               # Current frontend
    ├── detomo_logo.svg          # Branding
    └── js/css/                  # JS and CSS files
```

---

## RESOURCES

### Documentation Links
- **Vanna AI Docs**: https://vanna.ai/docs/
- **Claude Agent SDK**: https://github.com/anthropics/claude-agent-sdk
- **Anthropic API**: https://docs.anthropic.com/
- **ChromaDB Docs**: https://docs.trychroma.com/
- **Flask Docs**: https://flask.palletsprojects.com/
- **Plotly Docs**: https://plotly.com/python/

### Reference Repositories
- **vanna-flask**: https://github.com/vanna-ai/vanna-flask
- **Chinook Database**: https://github.com/lerocha/chinook-database

### Internal References
- **PRD**: [docs/PRD.md](docs/PRD.md)
- **Task Master**: [TASK_MASTER.md](TASK_MASTER.md)
- **Task Files**: [tasks/](tasks/)

---

## FINAL NOTES

### Best Practices
1. **Read before coding**: Always read the task file completely before starting
2. **Test frequently**: Run tests after each significant change
3. **Commit often**: Use git commits to save progress incrementally
4. **Ask questions**: If task requirements are unclear, ask for clarification
5. **Document decisions**: Add comments explaining why, not just what

### Success Metrics
- Code coverage ≥ 80%
- All tests passing
- SQL accuracy ≥ 85%
- Response time < 5s (p95)
- No critical bugs

### Getting Help
If you encounter issues not covered in this guide:
1. Check the specific task file for task-related guidance
2. Review PRD for architectural decisions
3. Check TASK_MASTER.md for dependencies
4. Review completed task files for implementation patterns
5. Consult external documentation (Vanna, Claude, Flask)

---

**Good luck with the implementation!**

Remember: Quality over speed. Take time to write clean, tested, documented code.

---

**Last Updated**: 2025-10-26
