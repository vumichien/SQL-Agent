# CLAUDE.md - Instructions for Claude Code Assistant

**Project**: Detomo SQL AI
**Version**: 1.2
**Date**: 2025-10-26
**Database**: SQLite (data/chinook.db)

---

## 📁 File Organization Rules

**IMPORTANT**: Follow these rules strictly when creating or organizing files.

### Root Directory (Only 3 Core Files)
```
SQL-Agent/
├── README.md          # Project overview and quick start
├── TASK_MASTER.md     # Project progress tracker
└── CLAUDE.md          # This file - Instructions for Claude
```

**Rule**: Keep root clean! Only these 3 files + PRD.md allowed in root.

### All Documentation → `docs/`

**Rule**: ALL documentation files created during development must go to `docs/` with appropriate subdirectory:

```
docs/
├── api/               # API documentation
│   ├── API_DOCUMENTATION.md
│   └── BACKEND_SWITCHING.md
├── guides/            # User guides and tutorials
│   └── QUICKSTART_API.md
└── development/       # Development documentation
    ├── TASK_XX_SUMMARY.md        # Task completion summaries
    ├── PROJECT_STRUCTURE.md       # Detailed structure docs
    └── REORGANIZATION_SUMMARY.md  # Change logs
```

### Scripts → `scripts/`

**Rule**: All utility scripts go to `scripts/`:
- Training scripts (train_*.py)
- Verification scripts (verify_*.py, check_*.py)
- Database scripts (reset_*.py)
- Any automation scripts

### Tests → `tests/`

**Rule**: Organize tests by type:
```
tests/
├── unit/          # Unit tests (individual components)
├── integration/   # Integration tests (components together)
└── e2e/          # End-to-end tests (future)
```

### When Creating New Files

1. **Documentation** → Always create in `docs/` with appropriate subdirectory
2. **Scripts** → Always create in `scripts/`
3. **Tests** → Create in `tests/unit/` or `tests/integration/`
4. **Source Code** → Create in `src/`, `api/`, or `backend/`

### Examples

✅ **Correct**:
- Task summary → `docs/development/TASK_06_SUMMARY.md`
- API guide → `docs/api/ENDPOINTS.md`
- Verification script → `scripts/verify_api.py`
- Unit test → `tests/unit/test_config.py`

❌ **Wrong**:
- `TASK_06_SUMMARY.md` (root)
- `API_GUIDE.md` (root)
- `verify_api.py` (root)
- `test_something.py` (root)

**Remember**: Clean root = Professional project!

---

## 🚀 Quick Start

### To Start Working on Tasks:

**Just type**: `start`

Claude will:
1. Check current progress in TASK_MASTER.md
2. Find the next incomplete task
3. Read the task file
4. Execute all steps automatically
5. Verify completion
6. Update progress
7. Move to next task

---

## 📋 Manual Commands

| Command | Description |
|---------|-------------|
| `start` | Auto-execute next task |
| `start task 01` | Execute specific task |
| `status` | Show current progress |
| `verify` | Verify current task completion |
| `next` | Skip to next task |

---

## 🤖 Auto-Execution Mode

When you say **"start"**, Claude will:

### Step 1: Analyze Current State
```
- Read TASK_MASTER.md
- Find current/next task
- Check dependencies completed
- Verify prerequisites
```

### Step 2: Execute Task
```
- Read task file (tasks/TASK_XX_*.md)
- Execute all implementation steps
- Run verification scripts
- Test deliverables
```

### Step 3: Update Progress
```
- Mark task as completed in TASK_MASTER.md
- Update completion percentage
- Record completion date
- Note any issues
```

### Step 4: Continue or Stop
```
- If more tasks: Ask "Continue to next task?"
- If blocked: Report issue and stop
- If complete: Celebrate! 🎉
```

---

## 📊 Current Project Status

**Database Type**: SQLite (Updated from PostgreSQL)
**Location**: `data/chinook.db`
**Total Tasks**: 12
**Completed**: 2/12 (17%)
**Current Phase**: Phase 1 - Foundation

**Key Changes**:
- ✅ Using SQLite instead of PostgreSQL (simpler setup!)
- ✅ Database already exists at data/chinook.db
- ✅ Task 01 reduced from 2h to 30min
- ✅ Table names: lowercase (albums, customers, invoice_items)
- ✅ Using `uv` for virtual environment management

---

## 🔧 Setup Virtual Environment

This project uses `uv` for fast and efficient Python environment management.

### Initial Setup
```bash
# Create virtual environment
uv venv

# Activate virtual environment
# On Windows (Git Bash):
source .venv/Scripts/activate

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# On Linux/Mac:
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

### Running the Project
Always activate the virtual environment before running any Python scripts:
```bash
# Activate
source .venv/Scripts/activate  # Windows Git Bash
# or
source .venv/bin/activate       # Linux/Mac

# Run tests
PYTHONPATH=. python tests/test_detomo_vanna.py

# Run training scripts (later)
python scripts/train_chinook.py
```

**Note**: The `.venv/` directory is already in `.gitignore` and should not be committed.

---

## Overview

This document provides step-by-step instructions for Claude Code Assistant to execute tasks in the Detomo SQL AI project. Each task has detailed implementation steps, verification criteria, and update procedures.

---

## General Workflow

For each task, follow this workflow:

```
1. Read Task File (tasks/TASK_XX_name.md)
2. Verify Prerequisites
3. Execute Implementation Steps
4. Verify Completion Criteria
5. Update TASK_MASTER.md
6. Update This File (CLAUDE.md)
7. Move to Next Task
```

---

## Task Execution Guide

### 🔴 PHASE 1: FOUNDATION

---

## TASK 01: Verify Chinook Database

**File**: `tasks/TASK_01_setup_chinook_database.md`
**Estimate**: 30 minutes
**Database**: SQLite (data/chinook.db)

### Execution Steps

#### Step 1: Verify Database File Exists
```bash
# Check if database file exists
ls -la data/chinook.db

# Expected: File size ~884KB
```

#### Step 2: Create Test Scripts
Create verification scripts to test database:

**File: `verify_db.py`**
```python
import sqlite3

def verify_database():
    print("Verifying Chinook Database...")

    # Connect to database
    conn = sqlite3.connect('data/chinook.db')
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    tables = [row[0] for row in cursor.fetchall()]

    print(f"\n✓ Found {len(tables)} tables:")

    # Count rows in each table
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  - {table}: {count:,} rows")

    # Test sample queries
    print("\nTesting sample queries:")

    # Query 1: Total customers
    cursor.execute("SELECT COUNT(*) FROM customers")
    print(f"  ✓ Total customers: {cursor.fetchone()[0]}")

    # Query 2: Total revenue
    cursor.execute("SELECT SUM(Total) FROM invoices")
    revenue = cursor.fetchone()[0]
    print(f"  ✓ Total revenue: ${revenue:,.2f}")

    # Query 3: Top artist
    cursor.execute("""
        SELECT ar.Name, COUNT(al.AlbumId) as albums
        FROM artists ar
        JOIN albums al ON ar.ArtistId = al.ArtistId
        GROUP BY ar.ArtistId
        ORDER BY albums DESC
        LIMIT 1
    """)
    top_artist = cursor.fetchone()
    print(f"  ✓ Top artist: {top_artist[0]} ({top_artist[1]} albums)")

    conn.close()
    print("\n✅ Database verification completed successfully!")
    return True

if __name__ == "__main__":
    verify_database()
```

#### Step 3: Run Verification
```bash
# Run verification script
python verify_db.py
```

**Expected Output**:
```
Verifying Chinook Database...

✓ Found 11 tables:
  - albums: 347 rows
  - artists: 275 rows
  - customers: 59 rows
  - employees: 8 rows
  - genres: 25 rows
  - invoice_items: 2,240 rows
  - invoices: 412 rows
  - media_types: 5 rows
  - playlist_track: 8,715 rows
  - playlists: 18 rows
  - tracks: 3,503 rows

Testing sample queries:
  ✓ Total customers: 59
  ✓ Total revenue: $2,328.60
  ✓ Top artist: Iron Maiden (21 albums)

✅ Database verification completed successfully!
```

#### Step 4: Create .env File
```bash
# Create .env in project root
cat > .env << 'EOF'
# Database Configuration (SQLite)
DB_TYPE=sqlite
DB_PATH=data/chinook.db

# LLM Configuration (for later use)
ANTHROPIC_API_KEY=

# Application Settings
FLASK_ENV=development
FLASK_DEBUG=True
LOG_LEVEL=INFO
EOF
```

#### Step 5: Test Database Connection
```python
# Quick test
python -c "
import sqlite3
conn = sqlite3.connect('data/chinook.db')
print('✓ Database connection successful')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM customers')
print(f'✓ Customers: {cursor.fetchone()[0]}')
conn.close()
"
```

### Verification Checklist
- [ ] File `data/chinook.db` exists (884KB)
- [ ] Database opens with sqlite3
- [ ] All 11 tables present
- [ ] Row counts correct (customers=59, albums=347, etc.)
- [ ] Sample queries execute successfully
- [ ] JOIN queries work
- [ ] Aggregation queries work
- [ ] `.env` file created with DB_PATH
- [ ] verify_db.py script runs successfully

### Update TASK_MASTER.md
After completion, update task status:
```markdown
#### ✅ Task 01: Verify Chinook Database
- **Status**: ✅ Completed
- **Completion**: ☑ 100%
- **Completed Date**: [DATE]
- **Notes**: SQLite database verified with 11 tables, 15,000+ total rows
```

### Next Task
➡️ Proceed to TASK 02

---

## TASK 02: Create Training Data Files

**File**: `tasks/TASK_02_create_training_data.md`
**Estimate**: 16 hours

### Execution Steps

#### Step 1: Create Directory Structure
```bash
mkdir -p training_data/chinook/{ddl,documentation,questions}
```

#### Step 2: Extract DDL Files
```bash
# For each table, extract DDL
psql -U postgres -d chinook

# Use \d+ table_name and save to file
# Example for Customer table:
\d+ Customer > temp_customer_ddl.txt

# Create clean DDL file: training_data/chinook/ddl/customer.sql
# Repeat for all 11 tables:
# album, artist, customer, employee, genre, invoice, invoice_line,
# media_type, playlist, playlist_track, track
```

**Claude Action**: Use the Write tool to create each DDL file based on the table structure.

Example template:
```sql
CREATE TABLE Customer (
    CustomerId INTEGER PRIMARY KEY,
    FirstName VARCHAR(40) NOT NULL,
    LastName VARCHAR(20) NOT NULL,
    -- ... (add all columns)
);
```

#### Step 3: Create Documentation Files
**Claude Action**: For each table, create a documentation file in `training_data/chinook/documentation/`.

Template structure:
```markdown
# [Table Name]

## Description
[Purpose of the table]

## Columns
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ... | ... | ... | ... |

## Relationships
- [Describe relationships]

## Business Rules
1. [Rule 1]
2. [Rule 2]

## Common Query Patterns
[Example queries]

## Japanese Terminology
- [English term] = [Japanese term]
```

Create files for:
- customer.md, invoice.md, invoice_line.md, track.md, album.md, artist.md,
- genre.md, playlist.md, employee.md, media_type.md, business_rules.md

#### Step 4: Create Q&A JSON Files
**Claude Action**: Create 4 JSON files with question-answer pairs.

**File 1**: `training_data/chinook/questions/basic_queries.json`
```json
[
  {
    "question": "How many customers are there?",
    "sql": "SELECT COUNT(*) FROM Customer"
  },
  {
    "question": "顧客は何人いますか？",
    "sql": "SELECT COUNT(*) FROM Customer"
  }
  // Add 18 more basic queries
]
```

**File 2**: `training_data/chinook/questions/aggregation_queries.json`
- 15 aggregation queries (SUM, AVG, COUNT, GROUP BY)

**File 3**: `training_data/chinook/questions/join_queries.json`
- 15 join queries (INNER JOIN, LEFT JOIN, multiple joins)

**File 4**: `training_data/chinook/questions/japanese_queries.json`
- 20 queries in Japanese

### Verification
- [ ] Directory structure created
- [ ] 11 DDL files + 1 relationships file (12 total)
- [ ] 10 table docs + 1 business rules (11 total)
- [ ] 4 Q&A JSON files with 70+ total questions
- [ ] All JSON files valid (use `jq` to validate)
- [ ] Japanese characters display correctly (UTF-8)
- [ ] All SQL queries tested and working

### Update TASK_MASTER.md
```markdown
#### ✅ Task 02: Create Training Data Files
- **Status**: ✅ Completed
- **Completion**: ☑ 100%
- **Completed Date**: [DATE]
- **Notes**: Created 12 DDL, 11 docs, 70+ Q&A pairs
```

### Next Task
➡️ Proceed to TASK 03

---

## TASK 03: Implement DetomoVanna Class

**File**: `tasks/TASK_03_implement_detomo_vanna.md`
**Estimate**: 8 hours

### Execution Steps

#### Step 1: Install Dependencies
```bash
# Create requirements.txt
cat > requirements.txt << 'EOF'
vanna==0.7.9
anthropic>=0.40.0
chromadb<1.0.0
psycopg2-binary
langchain-huggingface
sentence-transformers
python-dotenv
flask>=3.0.0
flask-cors
pandas
plotly
pytest
EOF

# Install
pip install -r requirements.txt
```

#### Step 2: Create Project Structure
```bash
mkdir -p src tests
touch src/__init__.py
touch src/config.py
touch src/detomo_vanna_dev.py
touch src/detomo_vanna_prod.py
touch tests/__init__.py
touch tests/test_detomo_vanna.py
```

#### Step 3: Implement Configuration
**Claude Action**: Create `src/config.py` with the configuration code from TASK_03.

Key components:
- Load environment variables from .env
- Database connection settings
- LLM settings (model, temperature, max_tokens)
- Vector DB settings
- DevelopmentConfig and ProductionConfig classes

#### Step 4: Implement DetomoVanna Development Class
**Claude Action**: Create `src/detomo_vanna_dev.py`

Key components:
- Inherit from ChromaDB_VectorStore and ClaudeAgentChat/Anthropic_Chat
- Initialize with config
- connect_to_database() method
- get_training_stats() method
- Factory function create_vanna_dev()

#### Step 5: Implement DetomoVanna Production Class
**Claude Action**: Create `src/detomo_vanna_prod.py`

Similar to dev but uses Anthropic_Chat directly.

#### Step 6: Create Tests
**Claude Action**: Create `tests/test_detomo_vanna.py`

Test cases:
- test_vanna_initialization()
- test_database_connection()
- test_training_stats()

#### Step 7: Run Tests
```bash
# Run tests
pytest tests/test_detomo_vanna.py -v

# Test manually
python -c "
from src.detomo_vanna_dev import create_vanna_dev
vn = create_vanna_dev()
print('Connection test:', vn.run_sql('SELECT COUNT(*) FROM Customer'))
print('Training stats:', vn.get_training_stats())
"
```

### Verification
- [ ] All dependencies installed
- [ ] Project structure created
- [ ] src/config.py working
- [ ] src/detomo_vanna_dev.py working
- [ ] src/detomo_vanna_prod.py working
- [ ] Tests passing
- [ ] Can connect to database
- [ ] Can query database

### Update TASK_MASTER.md
```markdown
#### ✅ Task 03: Implement DetomoVanna Class
- **Status**: ✅ Completed
- **Completion**: ☑ 100%
- **Completed Date**: [DATE]
- **Notes**: Both dev and prod classes implemented, tests passing
```

### Next Task
➡️ Proceed to TASK 04

---

## TASK 04: Training Script Implementation

**File**: `tasks/TASK_04_training_script.md`
**Estimate**: 4 hours

### Execution Steps

#### Step 1: Create Scripts
```bash
mkdir -p scripts
touch scripts/__init__.py
touch scripts/train_chinook.py
touch scripts/reset_training.py
touch scripts/check_training.py
```

#### Step 2: Implement Training Script
**Claude Action**: Create `scripts/train_chinook.py` with the code from TASK_04.

Key components:
- ChinookTrainer class
- train_ddl() method
- train_documentation() method
- train_questions() method
- verify_training() method
- main() function

#### Step 3: Implement Helper Scripts
**Claude Action**:
- Create `scripts/reset_training.py` - removes vector DB
- Create `scripts/check_training.py` - shows training stats

#### Step 4: Make Executable
```bash
# Windows - not needed
# Linux/Mac
chmod +x scripts/*.py
```

#### Step 5: Run Training
```bash
# Run training script
python scripts/train_chinook.py

# This will:
# 1. Load all DDL files
# 2. Load all documentation files
# 3. Load all Q&A pairs
# 4. Verify training data
# 5. Show summary

# Expected time: 5-10 minutes
```

#### Step 6: Verify Training
```bash
# Check training stats
python scripts/check_training.py

# Expected output:
# Total items: 90+
# DDL: 12
# Documentation: 11
# SQL/Q&A: 70+
```

#### Step 7: Test SQL Generation
```bash
python -c "
from src.detomo_vanna_dev import create_vanna_dev

vn = create_vanna_dev()

# Test questions
questions = [
    'How many customers are there?',
    '顧客は何人いますか？',
    'Top 10 customers by revenue'
]

for q in questions:
    print(f'\nQuestion: {q}')
    try:
        sql = vn.generate_sql(q)
        print(f'SQL: {sql}')
    except Exception as e:
        print(f'Error: {e}')
"
```

### Verification
- [ ] Scripts created
- [ ] train_chinook.py runs without errors
- [ ] All training data loaded (90+ items)
- [ ] Vector database created (detomo_vectordb/ folder)
- [ ] check_training.py shows correct stats
- [ ] Can generate SQL from natural language
- [ ] Generated SQL is valid

### Update TASK_MASTER.md
```markdown
#### ✅ Task 04: Training Script Implementation
- **Status**: ✅ Completed
- **Completion**: ☑ 100%
- **Completed Date**: [DATE]
- **Notes**: Training completed with [X] items, SQL generation working
```

### Next Task
➡️ Proceed to TASK 05

---

## TASK 05: Flask API Development

**File**: `tasks/TASK_05_flask_api.md`
**Estimate**: 16 hours

### Execution Steps

#### Step 1: Create Flask App Structure
```bash
mkdir -p api static templates
touch app.py
touch api/__init__.py
touch api/routes.py
touch api/errors.py
```

#### Step 2: Implement Main Flask App
**Claude Action**: Create `app.py` with Flask application setup.

Key endpoints to implement:
1. `POST /api/v0/generate_sql` - Generate SQL from question
2. `POST /api/v0/run_sql` - Execute SQL query
3. `POST /api/v0/generate_plotly_figure` - Generate chart
4. `GET /api/v0/get_training_data` - List training data
5. `POST /api/v0/train` - Add training data
6. `DELETE /api/v0/remove_training_data` - Remove training data

#### Step 3: Implement Error Handling
**Claude Action**: Create `api/errors.py` with error handlers.

#### Step 4: Add Logging
Configure logging for debugging and monitoring.

#### Step 5: Run Flask App
```bash
# Development mode
python app.py

# Should start on http://localhost:5000
```

#### Step 6: Test Endpoints
```bash
# Test generate_sql
curl -X POST http://localhost:5000/api/v0/generate_sql \
  -H "Content-Type: application/json" \
  -d '{"question": "How many customers?"}'

# Test run_sql
curl -X POST http://localhost:5000/api/v0/run_sql \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT COUNT(*) FROM Customer"}'
```

#### Step 7: Create API Tests
**Claude Action**: Create `tests/test_api.py` with endpoint tests.

### Verification
- [ ] Flask app runs without errors
- [ ] All 6 endpoints implemented
- [ ] generate_sql endpoint works
- [ ] run_sql endpoint works
- [ ] Error handling works
- [ ] Logging configured
- [ ] API tests pass
- [ ] CORS enabled

### Update TASK_MASTER.md
```markdown
#### ✅ Task 05: Flask API Development
- **Status**: ✅ Completed
- **Completion**: ☑ 100%
- **Completed Date**: [DATE]
- **Notes**: 6 API endpoints implemented, all tests passing
```

### Next Task
➡️ Proceed to TASK 06

---

## TASK 06-12: Remaining Tasks

For remaining tasks (06-12), follow the same pattern:

1. **Read task file** in `tasks/` folder
2. **Execute implementation steps** as described
3. **Verify completion** against checklist
4. **Update TASK_MASTER.md** with progress
5. **Move to next task**

---

## Progress Tracking Commands

### Check Overall Progress
```bash
# Count completed tasks
grep "Status.*Completed" TASK_MASTER.md | wc -l

# View task summary
grep -A 1 "Task [0-9][0-9]:" TASK_MASTER.md | grep -E "(Task|Status)"
```

### Update Task Status
When completing a task, update TASK_MASTER.md:
```markdown
# Change from:
- **Status**: ⏸️ Not Started
- **Completion**: ☐ 0%

# To:
- **Status**: ✅ Completed
- **Completion**: ☑ 100%
- **Completed Date**: 2025-10-25
```

### Update Phase Progress
Calculate phase completion percentage:
```
Completion % = (Completed Tasks / Total Tasks in Phase) * 100
```

---

## Testing Checklist

After each task, verify:
- [ ] Code runs without errors
- [ ] All files created as specified
- [ ] Tests pass (if applicable)
- [ ] Documentation updated
- [ ] TASK_MASTER.md updated
- [ ] Ready for next task

---

## Common Issues & Solutions

### Issue: Database Connection Fails
**Solution**:
```bash
# Check .env file
cat .env

# Test connection
psql -U detomo_reader -d chinook -h localhost

# Check PostgreSQL running
pg_ctl status
```

### Issue: Import Errors
**Solution**:
```bash
# Check Python environment
python --version

# Reinstall dependencies
pip install -r requirements.txt

# Check installations
pip list | grep vanna
```

### Issue: Training Takes Too Long
**Solution**: This is normal for first training (5-10 minutes). Be patient.

### Issue: SQL Generation Not Accurate
**Solution**:
- Add more training data (Q&A pairs)
- Check training data loaded correctly
- Review generated SQL and add corrections to training

---

## Quality Standards

### Code Quality
- Follow PEP 8 style guide
- Add docstrings to all functions
- Handle errors gracefully
- Log important events

### Documentation
- Update README.md with setup instructions
- Comment complex code sections
- Keep TASK_MASTER.md up to date
- Document API endpoints

### Testing
- Write tests for all core functionality
- Aim for ≥80% code coverage
- Test both success and error cases
- Verify SQL accuracy ≥85%

---

## Daily Workflow

### Start of Day
1. Review TASK_MASTER.md
2. Check current task status
3. Read task file for today's work
4. Set up development environment

### During Development
1. Follow task implementation steps
2. Test frequently
3. Commit code regularly
4. Update progress in TASK_MASTER.md

### End of Day
1. Complete verification checklist
2. Update TASK_MASTER.md
3. Commit all changes
4. Note any blockers or issues

---

## Communication

### Status Updates
Update TASK_MASTER.md with:
- Task progress (percentage)
- Completion date (when done)
- Notes (any issues or important info)
- Blockers (if stuck)

### Asking for Help
If blocked:
1. Document the issue
2. Mark task as ⏳ Blocked in TASK_MASTER.md
3. Note the reason
4. Request assistance

---

## Success Criteria

### Task Completion
A task is considered complete when:
- ✅ All implementation steps executed
- ✅ All verification items checked
- ✅ Tests passing (if applicable)
- ✅ Documentation updated
- ✅ TASK_MASTER.md updated
- ✅ Ready for next task

### Project Completion
Project is complete when:
- ✅ All 12 tasks marked as completed
- ✅ MVP requirements met (see TASK_MASTER.md)
- ✅ SQL accuracy ≥ 85%
- ✅ All tests passing
- ✅ Documentation complete
- ✅ Deployed to production

---

## Next Steps After Completion

Once all tasks are complete:
1. Conduct final testing
2. Create demo video
3. Prepare launch materials
4. Deploy to production
5. Monitor performance
6. Gather user feedback
7. Plan v2.0 features

---

## Reference Documents

- **PRD.md** - Product Requirements Document
- **TASK_MASTER.md** - Overall progress tracking
- **tasks/TASK_XX_*.md** - Individual task details
- **README.md** - Project overview and setup

---

**Last Updated**: 2025-10-25
**Current Task**: Task 01 (Not Started)
**Overall Progress**: 0% (0/12 tasks completed)
