# Detomo SQL AI 🤖

**AI-Powered Text-to-SQL Application** - Monorepo (Backend + Vue3 Frontend)

Convert natural language questions to SQL queries, execute them, and get visualizations automatically.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.120+-green.svg)](https://fastapi.tiangolo.com/)
[![Vue3](https://img.shields.io/badge/Vue-3.0+-brightgreen.svg)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-82%20Passing-brightgreen.svg)](#testing)
[![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)](#testing)

---

## ✨ Features

- 🧠 **AI-Powered SQL Generation**: Uses Claude Sonnet 4.5 for accurate SQL generation
- 🔍 **RAG-Enhanced**: ChromaDB vector store retrieves relevant schema and examples
- 📊 **Auto-Visualization**: Generates Plotly charts automatically from query results
- 🌍 **Bilingual**: Supports both English and Japanese questions
- ⚡ **Fast**: Response time < 5s (p95), 100% SQL accuracy on test queries
- 🎨 **Modern UI**: Clean, dark-mode web interface
- 🔌 **REST API**: 14 endpoints for flexible integration
- 📚 **Training Data Management**: Add/remove examples via API
- 🐳 **Docker Ready**: Easy deployment with Docker & docker-compose
- ☁️ **Cloud Ready**: Deploy to AWS, GCP, Azure, or Heroku

---

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

### Prerequisites

- **Python 3.10+** (for backend)
- **Node.js 20+** (for frontend)
- **Anthropic API key** ([Get one here](https://console.anthropic.com))
- **Docker & Docker Compose** (optional, recommended)

---

### Option 1: Docker Compose (Recommended - Chạy cả FE và BE)

**Chạy toàn bộ ứng dụng (Backend + Frontend) với 1 lệnh:**

```bash
# 1. Clone repository
git clone https://github.com/detomo/sql-ai.git
cd sql-ai

# 2. Configure backend environment
cd backend
cp .env.example .env
nano .env  # Add your ANTHROPIC_API_KEY
cd ..

# 3. Start cả Backend và Frontend với Docker Compose
docker-compose up

# Hoặc chạy ngầm (background):
docker-compose up -d

# Xem logs:
docker-compose logs -f

# Dừng services:
docker-compose down
```

**Access points:**
- **Frontend (Vue3)**: http://localhost:5173
- **Backend (FastAPI)**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

**✨ Training data tự động load lần đầu chạy! Không cần setup thêm.**

---

### Option 2: Local Development (Chạy Backend và Frontend riêng)

#### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
nano .env  # Add your ANTHROPIC_API_KEY

# 5. Load training data
python scripts/train_chinook.py

# 6. Start backend server
python main.py
# Hoặc: uvicorn app.main:app --reload
```

**Backend sẽ chạy tại**: http://localhost:8000

#### Frontend Setup (Terminal mới)

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
```

**Frontend sẽ chạy tại**: http://localhost:5173

---

### Option 3: Production Deployment (Docker Compose Production)

```bash
# 1. Configure production environment
cp .env.production.example .env.production
nano .env.production  # Add production settings

# 2. Build and start production containers
docker-compose -f docker-compose.prod.yml up -d

# 3. Load training data (first time)
docker exec -it detomo-backend-prod bash
python scripts/train_chinook.py
exit
```

**Access points (Production):**
- **Frontend**: http://localhost (port 80)
- **Backend**: http://localhost:8000

---

### Access Application

**Web UI**: http://localhost:8000

**API Docs**: http://localhost:8000/docs

**Health Check**: http://localhost:8000/api/v0/health

---

## 💡 Usage Examples

### Web UI

1. Open http://localhost:8000 in your browser
2. Type a question in the chat input (e.g., "How many customers are there?")
3. View the generated SQL, results table, and chart
4. Click on history items to reload previous queries

### REST API

**All-in-One Query**:
```bash
curl -X POST http://localhost:8000/api/v0/query \
  -H "Content-Type: application/json" \
  -d '{"question": "List the top 5 customers by total spending"}'
```

**Multi-Step Workflow**:
```bash
# Step 1: Generate SQL
response=$(curl -X POST http://localhost:8000/api/v0/generate_sql \
  -H "Content-Type: application/json" \
  -d '{"question": "How many tracks per genre?"}')
id=$(echo $response | jq -r '.id')

# Step 2: Execute SQL
curl -X POST http://localhost:8000/api/v0/run_sql \
  -H "Content-Type: application/json" \
  -d "{\"id\": \"$id\"}"

# Step 3: Generate visualization
curl -X POST http://localhost:8000/api/v0/generate_plotly_figure \
  -H "Content-Type: application/json" \
  -d "{\"id\": \"$id\"}"
```

**Python Client**:
```python
import requests

BASE_URL = "http://localhost:8000"

def query(question: str):
    response = requests.post(
        f"{BASE_URL}/api/v0/query",
        json={"question": question}
    )
    return response.json()

# Example
result = query("How many customers are there?")
print(f"SQL: {result['sql']}")
print(f"Results: {result['results']}")
```

---

## 🏗️ Architecture

```
┌─────────────────┐
│   Web UI (SPA)  │  React/Vue interface
└────────┬────────┘
         │ HTTP
┌────────▼────────┐
│  FastAPI Server │  14 REST endpoints
├─────────────────┤
│  DetomoVanna    │  Vanna AI + Claude Agent SDK
├─────────────────┤
│  ChromaDB       │  Vector store (RAG)
└─────────────────┘
         │
┌────────▼────────┐
│ SQLite/Postgres │  Target database
└─────────────────┘
```

**Components**:
- **FastAPI**: High-performance async web framework
- **Vanna AI**: Text-to-SQL RAG framework
- **Claude Agent SDK**: LLM interface (Claude Sonnet 4.5)
- **ChromaDB**: Vector database for embeddings
- **SQLite**: Demo database (Chinook music store)

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Architecture](docs/ARCHITECTURE.md) | System design, components, and data flow |
| [API Reference](docs/API_DOCUMENTATION.md) | All 14 endpoints with examples |
| [Deployment Guide](docs/DEPLOYMENT.md) | Production deployment, Docker, cloud platforms |
| [QA Report](docs/QA_REPORT.md) | Test results, accuracy metrics, benchmarks |
| [PRD](docs/PRD.md) | Product requirements and specifications |
| [Task Master](TASK_MASTER.md) | Development progress (11/12 tasks completed) |

---

## 🎯 Key Metrics

Based on comprehensive testing (TASK 11):

| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| SQL Accuracy | **100%** (20/20 queries) | ≥85% | ✅ **Exceeds** |
| Mean Response Time | **4.57s** | <5s | ✅ **Meets** |
| P95 Response Time | **5.54s** | <5s | ⚠️ Slightly above |
| Test Coverage | **100%** (src/) | ≥80% | ✅ **Exceeds** |
| Tests Passing | **82/82** | All | ✅ **Pass** |
| Overall Quality | **95/100** | - | ✅ **Production Ready** |

---

## 🧪 Testing

### Run Tests

```bash
# Navigate to backend
cd backend

# Activate virtual environment
source .venv/bin/activate

# Run all tests
PYTHONPATH=. pytest

# Run with coverage
PYTHONPATH=. pytest --cov=src --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Test Structure

```
backend/tests/
├── unit/                    # Unit tests (42 tests)
│   ├── test_agent_endpoint.py    # LLM endpoint tests
│   ├── test_detomo_vanna.py      # Vanna integration tests
│   └── test_cache.py             # Cache functionality tests
└── integration/             # Integration tests (40 tests)
    ├── test_training.py          # Training pipeline tests
    ├── test_api_core.py          # Core API endpoints
    └── test_api_extended.py      # Extended API endpoints
```

---

## 🛠️ Technology Stack

### Backend
- **Python 3.10+**: Programming language
- **FastAPI**: Web framework
- **Vanna AI 0.7.9**: Text-to-SQL framework
- **Claude Agent SDK**: LLM interface
- **ChromaDB**: Vector database
- **pandas**: Data processing
- **Plotly**: Visualization

### Frontend (Migrating to Vue3 in Phase 7)
- **Vue 3**: Modern reactive framework (TASK_15+)
- **TypeScript**: Type safety
- **Element Plus**: UI component library
- **Pinia**: State management
- **Vite**: Build tool
- **Legacy**: Vanilla JS (currently served at /)

### Testing & DevOps
- **pytest**: Testing framework
- **Docker**: Containerization
- **nginx**: Reverse proxy
- **systemd**: Process management

---

## 📦 Deployment Options

### Local Development
```bash
cd backend
python claude_agent_server.py
```

### Docker
```bash
# From project root
docker-compose up backend -d
```

### Production (Ubuntu)
```bash
# Install as systemd service
sudo systemctl enable detomo-sql-ai
sudo systemctl start detomo-sql-ai
```

### Cloud Platforms
- **AWS**: Elastic Beanstalk, ECS, or Lambda
- **Google Cloud**: Cloud Run or App Engine
- **Azure**: Container Instances or App Service
- **Heroku**: Git-based deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment instructions.

---

## 🔧 Configuration

### Environment Variables

Create `backend/.env` file:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-your-api-key-here

# Optional (with defaults)
DATABASE_PATH=data/chinook.db
VECTOR_DB_PATH=./detomo_vectordb
CLAUDE_MODEL=claude-sonnet-4-5
CLAUDE_TEMPERATURE=0.1
CLAUDE_MAX_TOKENS=2048
SERVER_PORT=8000
LOG_LEVEL=info
```

### Custom Database

Connect to your own database:

```python
# In backend/claude_agent_server.py, replace:
vn.connect_to_sqlite("data/chinook.db")

# With PostgreSQL:
vn.connect_to_postgres(
    host="localhost",
    dbname="your_db",
    user="user",
    password="password"
)

# Or MySQL:
vn.connect_to_mysql(
    host="localhost",
    dbname="your_db",
    user="user",
    password="password"
)
```

---

## 📊 Database Schema

Uses **Chinook Database** (digital music store):

**Tables** (11 total):
- `Artist`, `Album`, `Track` (music catalog)
- `Genre`, `MediaType` (metadata)
- `Customer`, `Invoice`, `InvoiceLine` (sales)
- `Employee` (staff)
- `Playlist`, `PlaylistTrack` (playlists)

**Sample Questions**:
- "How many customers are there?"
- "List the top 10 albums by sales"
- "What are the most popular genres?"
- "Show total sales by country"
- "Which artists have the most tracks?"

---

## 🎓 Training Data

The system includes **93 training examples**:

- **12 DDL files**: CREATE TABLE statements with relationships
- **11 Documentation files**: Table/column descriptions (EN/JP)
- **70 Q&A pairs**: Example questions with SQL (EN/JP)

### Add Custom Training Data

**Via API**:
```bash
# Add Q&A pair
curl -X POST http://localhost:8000/api/v0/train \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How many products?",
    "sql": "SELECT COUNT(*) FROM Product"
  }'

# Add documentation
curl -X POST http://localhost:8000/api/v0/train \
  -H "Content-Type: application/json" \
  -d '{
    "documentation": "Product table contains all products..."
  }'
```

**Via Files**:
```bash
# Create training data files in backend
cd backend
mkdir -p training_data/my_db/{ddl,documentation,questions}

# Add your DDL, docs, and Q&A JSON files

# Run training script
python scripts/train_chinook.py
```

---

## 🐛 Troubleshooting

### Common Issues

**1. Port already in use**:
```bash
lsof -i :8000
kill -9 <PID>
```

**2. Module not found**:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**3. API key error**:
```bash
# Check .env file
cat .env | grep ANTHROPIC_API_KEY

# Set manually
export ANTHROPIC_API_KEY=sk-ant-your-key
```

**4. Database not found**:
```bash
# Re-download Chinook database
curl -o data/chinook.db https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite
```

See [docs/DEPLOYMENT.md#troubleshooting](docs/DEPLOYMENT.md#troubleshooting) for more solutions.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests before committing
pytest

# Run linter
flake8 src/ tests/

# Format code
black src/ tests/
```

---

## 📝 Changelog

### Version 3.0.0 (2025-10-27) - In Progress

**Phase 7: Frontend Migration** - Monorepo + Vue3 + TypeScript

**Completed (TASK_13)**:
- ✅ Monorepo structure created (/backend, /frontend, /shared)
- ✅ Backend code migrated to /backend directory
- ✅ Docker Compose configuration
- ✅ Documentation updated

**In Progress**:
- ⏳ TASK_14: Backend refactor (clean architecture + JWT auth)
- ⏳ TASK_15-28: Vue3 + TypeScript frontend (16 tasks)

**Goals**:
- Clean architecture for backend
- Modern Vue3 + TypeScript frontend
- Element Plus UI library
- Pinia state management
- JWT authentication
- Comprehensive E2E testing

### Version 2.0.0 (2025-10-26)

**Major Release** - Production Ready

**Features**:
- ✅ Unified FastAPI architecture (replaced Flask)
- ✅ 14 REST API endpoints (core + vanna-flask pattern)
- ✅ Web UI with chat interface
- ✅ Multi-step workflow with caching
- ✅ Bilingual support (EN/JP)
- ✅ 93 training examples loaded
- ✅ 100% SQL accuracy (20/20 test queries)
- ✅ 82 tests passing (42 unit + 40 integration)
- ✅ 100% test coverage for src/ modules
- ✅ Docker support
- ✅ Comprehensive documentation

**Performance**:
- Mean response time: 4.57s
- P95 response time: 5.54s
- Overall quality score: 95/100

---

## 🔐 Security

### Best Practices

- ✅ Environment variables for secrets (no hardcoded keys)
- ✅ Input validation with Pydantic
- ✅ SQL injection protection (parameterized queries)
- ⚠️ No authentication (MVP) - **add in production**
- ⚠️ CORS allows all origins - **restrict in production**

### Production Recommendations

- Add API key authentication
- Implement rate limiting
- Configure CORS for specific origins
- Use HTTPS with valid SSL certificates
- Set up firewall rules
- Enable logging and monitoring
- Regular security updates

See [docs/DEPLOYMENT.md#security](docs/DEPLOYMENT.md#security) for detailed security guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Vanna AI**: For the excellent Text-to-SQL framework
- **Anthropic**: For Claude Sonnet 4.5 (best SQL generation model)
- **Chinook Database**: For the demo database
- **FastAPI**: For the amazing web framework
- **ChromaDB**: For the vector database

---

## 📞 Support

Need help or have questions?

- **GitHub Issues**: [github.com/detomo/sql-ai/issues](https://github.com/detomo/sql-ai/issues)
- **Documentation**: [docs.detomo.com](https://docs.detomo.com)
- **Email**: support@detomo.com
- **Twitter**: [@DetomoAI](https://twitter.com/DetomoAI)

---

## 🗺️ Roadmap

### Phase 2 (Q2 2025)
- [ ] User authentication and authorization
- [ ] Multi-database support (connect multiple DBs)
- [ ] Query history persistence (save to database)
- [ ] Advanced visualizations (more chart types)
- [ ] Query optimization suggestions
- [ ] Natural language explanations of SQL

### Phase 3 (Q3 2025)
- [ ] Real-time collaboration
- [ ] Scheduled queries (cron-like)
- [ ] Data export (Excel, PDF, Google Sheets)
- [ ] Mobile app (iOS/Android)
- [ ] Voice input support
- [ ] Multi-tenancy for enterprises

---

## ⭐ Star History

If you find this project helpful, please consider giving it a star on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=detomo/sql-ai&type=Date)](https://star-history.com/#detomo/sql-ai&Date)

---

## 📈 Project Status

- **Version**: 3.0.0 (In Progress)
- **Status**: Phase 7 Migration - Backend Restructure Complete
- **Tasks Completed**: 13/28 (46%)
- **Backend Quality**: Production Ready (95/100 score)
- **Test Coverage**: 100% (backend/src/)
- **Tests Passing**: 82/82 (backend)
- **Last Updated**: 2025-10-27
- **Next Milestone**: TASK_14 (Backend Refactor)

---

**Made with ❤️ by the Detomo Team**

*Transforming natural language into SQL, one query at a time.*
