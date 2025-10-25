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

- 🤖 **AI-Powered**: Uses Claude 3.5 Sonnet for SQL generation
- 🌏 **Bilingual**: Supports Japanese and English queries
- 📊 **Auto Visualization**: Generates charts automatically with Plotly
- 🎯 **High Accuracy**: Target ≥85% SQL correctness
- ⚡ **Fast Response**: < 5 seconds for most queries
- 🔒 **Secure**: Read-only database access, SQL injection prevention

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **LLM** | Claude Agent SDK (dev) / Anthropic API (prod) |
| **RAG Framework** | Vanna AI |
| **Vector Database** | ChromaDB (dev) / PGVector (prod) |
| **Embedding Model** | BAAI/bge-m3 (HuggingFace) |
| **Target Database** | PostgreSQL (Chinook sample) |
| **Backend** | Python 3.10+, Flask |
| **Frontend** | Vanna-Flask (customized) |
| **Visualization** | Plotly |

---

## Quick Start

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- Git

### Installation

```bash
# 1. Clone repository
git clone https://github.com/detomo/sql-agent.git
cd sql-agent

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
# Edit .env with your database credentials

# 5. Setup Chinook database (see CLAUDE.md Task 01)
# Download and run Chinook PostgreSQL scripts

# 6. Train the model
python scripts/train_chinook.py

# 7. Run the application
python app.py
```

Visit http://localhost:5000 to use the application.

---

## Project Structure

```
sql-agent/
├── PRD.md                      # Product Requirements Document
├── TASK_MASTER.md              # Overall task tracking
├── CLAUDE.md                   # Execution guide for Claude
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── app.py                      # Flask application
│
├── tasks/                      # Individual task files
│   ├── TASK_01_setup_chinook_database.md
│   ├── TASK_02_create_training_data.md
│   ├── TASK_03_implement_detomo_vanna.md
│   ├── ... (12 tasks total)
│
├── src/                        # Source code
│   ├── __init__.py
│   ├── config.py               # Configuration
│   ├── detomo_vanna_dev.py     # Development class
│   └── detomo_vanna_prod.py    # Production class
│
├── scripts/                    # Utility scripts
│   ├── train_chinook.py        # Training script
│   ├── reset_training.py       # Reset vector DB
│   └── check_training.py       # Check training stats
│
├── training_data/              # Training data
│   └── chinook/
│       ├── ddl/                # Table definitions
│       ├── documentation/      # Table docs
│       └── questions/          # Q&A pairs
│
├── tests/                      # Test files
│   ├── test_detomo_vanna.py
│   └── test_api.py
│
├── api/                        # API routes
│   ├── __init__.py
│   ├── routes.py
│   └── errors.py
│
├── static/                     # Frontend assets
│   ├── css/
│   ├── js/
│   └── images/
│
└── templates/                  # HTML templates
    ├── base.html
    ├── chat.html
    └── admin.html
```

---

## Quick Links

- 📋 [Product Requirements (PRD.md)](PRD.md)
- 📊 [Task Master (TASK_MASTER.md)](TASK_MASTER.md)
- 🤖 [Claude Guide (CLAUDE.md)](CLAUDE.md)
- 📁 [Tasks Folder](tasks/)

---

## Getting Started

### For Team Members

1. **Read PRD**: Start with [PRD.md](PRD.md) for full requirements
2. **Review Tasks**: Check [TASK_MASTER.md](TASK_MASTER.md) for task overview
3. **Follow Tasks**: Execute tasks 01-12 in order (see [tasks/](tasks/) folder)
4. **Use CLAUDE.md**: Follow [CLAUDE.md](CLAUDE.md) for detailed execution steps

### For Claude Code Assistant

See [CLAUDE.md](CLAUDE.md) for comprehensive instructions on executing each task.

---

## Development Status

**Version**: 1.0.0
**Status**: In Development (0% complete)
**Start Date**: 2025-10-25
**Target Completion**: 8 weeks

**Phase 1**: Foundation (Tasks 01-04) - Not Started
**Phase 2**: API Development (Task 05) - Not Started
**Phase 3**: Frontend (Task 06) - Not Started
**Phase 4**: Testing & Optimization (Tasks 07-10) - Not Started
**Phase 5**: Deployment (Task 11) - Not Started
**Phase 6**: Polish & Launch (Task 12) - Not Started

---

## License

This project is licensed under the MIT License.

---

## Support

- **Documentation**: See [CLAUDE.md](CLAUDE.md) and [PRD.md](PRD.md)
- **Issues**: GitHub Issues
- **Email**: support@detomo.com

---

**Last Updated**: 2025-10-25