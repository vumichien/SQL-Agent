# TASK 13: Project Restructure - Monorepo Setup

**Status**: Not Started
**Estimated Time**: 4-6 hours
**Dependencies**: TASK 12 (Documentation complete)
**Priority**: High

---

## OVERVIEW

Restructure the project into a monorepo with separate `/backend` and `/frontend` folders. This sets the foundation for the Vue3 frontend migration while maintaining the existing backend functionality.

---

## OBJECTIVES

1. Create clean monorepo folder structure
2. Move existing backend code to `/backend`
3. Setup Docker Compose for development
4. Update all documentation
5. Ensure backward compatibility

---

## REQUIREMENTS

### Functional Requirements

1. **Folder Structure**:
   - Create `/backend` folder for FastAPI backend
   - Create `/frontend` folder (placeholder for now)
   - Create `/shared` folder for shared types/constants
   - Move existing code to appropriate folders

2. **Backend Migration**:
   - Move all Python files to `/backend`
   - Update import paths
   - Update config files
   - Ensure all tests still pass

3. **Docker Setup**:
   - Create `docker-compose.yml` for development
   - Separate containers for backend and frontend
   - Shared network configuration
   - Volume mounts for hot reload

4. **Documentation Updates**:
   - Update README.md with new structure
   - Update CLAUDE.md with new paths
   - Update all task references

---

## IMPLEMENTATION STEPS

### Step 1: Create Folder Structure

```bash
# Create new folders
mkdir -p backend
mkdir -p frontend
mkdir -p shared
mkdir -p backend/tests
mkdir -p backend/scripts
mkdir -p backend/src
mkdir -p backend/training_data
mkdir -p backend/data
```

### Step 2: Move Backend Files

```bash
# Move Python files
mv claude_agent_server.py backend/
mv src/* backend/src/
mv scripts/* backend/scripts/
mv tests/* backend/tests/
mv training_data/* backend/training_data/
mv data/* backend/data/

# Move config files
mv requirements.txt backend/
mv .env backend/
cp .env.example backend/

# Create backend README
touch backend/README.md
```

### Step 3: Update Import Paths

Update all Python files to use correct import paths:

**backend/claude_agent_server.py**:
```python
# Old:
from src.detomo_vanna import DetomoVanna
from src.cache import MemoryCache

# New (should still work with proper PYTHONPATH):
from src.detomo_vanna import DetomoVanna
from src.cache import MemoryCache
```

**backend/tests/** files:
```python
# Update test imports if needed
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

### Step 4: Create Docker Compose

**docker-compose.yml** (root):
```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    container_name: detomo-backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - /app/.venv  # Don't mount venv
    env_file:
      - ./backend/.env
    command: uvicorn claude_agent_server:app --host 0.0.0.0 --port 8000 --reload
    networks:
      - detomo-network

  # Frontend will be added in TASK_15
  # frontend:
  #   build:
  #     context: ./frontend
  #   ...

networks:
  detomo-network:
    driver: bridge
```

**backend/Dockerfile.dev**:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Command will be overridden by docker-compose
CMD ["uvicorn", "claude_agent_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 5: Update .gitignore

```.gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.venv/
venv/
ENV/
env/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Environment variables
.env
backend/.env
frontend/.env

# Databases
*.db
*.sqlite
*.sqlite3

# Logs
*.log

# OS
.DS_Store
Thumbs.db

# Node (for frontend)
node_modules/
dist/
.nuxt/
.output/

# Testing
.coverage
htmlcov/
.pytest_cache/
coverage/

# ChromaDB
detomo_vectordb/
backend/detomo_vectordb/
```

### Step 6: Update Documentation

**README.md** (root):
```markdown
# Detomo SQL AI v3.0

**AI-Powered Text-to-SQL Application** with Vue3 Frontend

## 📁 Project Structure

```
SQL-Agent/
├── backend/                # FastAPI Backend
│   ├── src/               # Source code
│   ├── tests/             # Backend tests
│   ├── scripts/           # Training scripts
│   ├── training_data/     # Training examples
│   ├── data/              # Databases
│   ├── claude_agent_server.py
│   └── requirements.txt
├── frontend/              # Vue3 Frontend (TASK_15)
├── shared/                # Shared types/constants
├── docker-compose.yml     # Development setup
└── README.md
```

## 🚀 Quick Start

### Development (Docker)

```bash
# Start backend
docker-compose up backend

# Access API
http://localhost:8000/docs
```

### Development (Local)

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python claude_agent_server.py

# Frontend (coming in TASK_15)
cd frontend
npm install
npm run dev
```

...
```

**backend/README.md**:
```markdown
# Detomo SQL AI - Backend

FastAPI backend with Vanna AI and Claude Agent SDK.

## Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add ANTHROPIC_API_KEY

# Run training
python scripts/train_chinook.py

# Start server
python claude_agent_server.py
```

## API Documentation

Access at: http://localhost:8000/docs

## Testing

```bash
# Run all tests
PYTHONPATH=. pytest

# With coverage
PYTHONPATH=. pytest --cov=src --cov-report=html
```

## Project Structure

```
backend/
├── claude_agent_server.py   # Main FastAPI app
├── src/
│   ├── detomo_vanna.py      # Vanna integration
│   └── cache.py             # Cache implementation
├── tests/
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── scripts/
│   └── train_chinook.py     # Training script
├── training_data/           # Training examples
└── data/                    # Databases
```

## Environment Variables

```env
ANTHROPIC_API_KEY=sk-ant-your-api-key
DATABASE_PATH=data/chinook.db
VECTOR_DB_PATH=./detomo_vectordb
```

## API Endpoints

See API documentation at `/docs` or check `docs/API_DOCUMENTATION.md`
```

### Step 7: Update CLAUDE.md

Update all paths in CLAUDE.md to reference the new structure:

```markdown
# Changed paths
- `claude_agent_server.py` → `backend/claude_agent_server.py`
- `src/` → `backend/src/`
- `tests/` → `backend/tests/`
- `requirements.txt` → `backend/requirements.txt`
etc.
```

### Step 8: Test Everything

```bash
# 1. Test backend locally
cd backend
source .venv/bin/activate
python claude_agent_server.py
# Should start on http://localhost:8000

# 2. Test Docker
cd ..
docker-compose up backend
# Should build and start successfully

# 3. Run backend tests
cd backend
PYTHONPATH=. pytest
# All tests should pass

# 4. Test API endpoints
curl http://localhost:8000/api/v0/health
# Should return health status
```

---

## FILE STRUCTURE

### Final Structure

```
SQL-Agent/
├── backend/
│   ├── claude_agent_server.py
│   ├── requirements.txt
│   ├── .env
│   ├── .env.example
│   ├── README.md
│   ├── Dockerfile.dev
│   ├── src/
│   │   ├── __init__.py
│   │   ├── detomo_vanna.py
│   │   └── cache.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── unit/
│   │   └── integration/
│   ├── scripts/
│   │   └── train_chinook.py
│   ├── training_data/
│   │   └── chinook/
│   └── data/
│       └── chinook.db
├── frontend/              # Placeholder for TASK_15
├── shared/                # Placeholder for shared code
├── docker-compose.yml
├── .gitignore
├── README.md
├── TASK_MASTER.md
├── CLAUDE.md
└── tasks/
```

---

## TESTING CHECKLIST

- [ ] Backend server starts from `/backend` folder
- [ ] All import paths work correctly
- [ ] All backend tests pass (82 tests)
- [ ] Docker Compose builds successfully
- [ ] Backend container runs and accessible on port 8000
- [ ] API endpoints work (`/api/v0/health`, `/api/v0/query`)
- [ ] Training script works from new location
- [ ] ChromaDB initializes correctly
- [ ] Documentation updated and accurate
- [ ] .gitignore includes all necessary entries

---

## SUCCESS CRITERIA

- ✅ Clean folder structure: `/backend`, `/frontend`, `/shared`
- ✅ Backend code moved to `/backend` and working
- ✅ All tests passing (82/82 tests)
- ✅ Docker Compose working for backend
- ✅ Documentation updated (README, CLAUDE.md)
- ✅ No breaking changes to existing functionality
- ✅ .gitignore updated

---

## DEPENDENCIES

- None (standalone task)

---

## NOTES

### Migration Checklist

1. ✅ Create folder structure
2. ✅ Move backend files
3. ✅ Update import paths
4. ✅ Create Docker Compose
5. ✅ Update .gitignore
6. ✅ Update README.md
7. ✅ Update CLAUDE.md
8. ✅ Test locally
9. ✅ Test with Docker
10. ✅ Run all tests

### Important

- Keep existing `static/` folder for now (will be removed in TASK_15)
- Don't break existing functionality
- All 82 tests must still pass
- API endpoints must work exactly as before

### Next Steps

After completing this task:
- TASK_14: Backend Refactor (clean architecture)
- TASK_15: Vue3 Frontend Setup

---

**Created**: 2025-10-27
**Last Updated**: 2025-10-27
