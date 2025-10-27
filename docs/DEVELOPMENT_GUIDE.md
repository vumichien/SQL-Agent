# Development Guide - Detomo SQL AI v3.0

**Hướng dẫn phát triển và chạy ứng dụng**

---

## 📋 Mục lục

1. [Môi trường phát triển](#môi-trường-phát-triển)
2. [Chạy với Docker Compose](#chạy-với-docker-compose)
3. [Chạy Local Development](#chạy-local-development)
4. [Cấu trúc dự án](#cấu-trúc-dự-án)
5. [Lệnh thường dùng](#lệnh-thường-dùng)
6. [Troubleshooting](#troubleshooting)

---

## Môi trường phát triển

### Yêu cầu hệ thống

**Backend:**
- Python 3.10 hoặc cao hơn
- pip hoặc uv (package manager)
- Virtual environment (venv)

**Frontend:**
- Node.js 20 hoặc cao hơn
- npm (đi kèm với Node.js)

**Optional:**
- Docker Desktop
- Docker Compose

**API Keys:**
- Anthropic API Key (Claude) - Đăng ký tại: https://console.anthropic.com

---

## Chạy với Docker Compose

### Cách 1: Chạy cả Backend và Frontend

**Đơn giản nhất - Khuyến nghị cho người mới:**

```bash
# 1. Clone repository
git clone <repo-url>
cd SQL-Agent

# 2. Configure backend environment
cd backend
cp .env.example .env
# Sửa file .env, thêm ANTHROPIC_API_KEY của bạn

cd ..

# 3. Start tất cả services (Backend + Frontend)
docker-compose up

# Hoặc chạy ngầm (không block terminal):
docker-compose up -d
```

**Kết quả:**
- Backend chạy tại: http://localhost:8000
- Frontend chạy tại: http://localhost:5173
- API Docs: http://localhost:8000/docs

**Xem logs:**
```bash
# Xem tất cả logs
docker-compose logs -f

# Chỉ xem backend logs
docker-compose logs -f backend

# Chỉ xem frontend logs
docker-compose logs -f frontend
```

**Dừng services:**
```bash
# Dừng nhưng giữ containers
docker-compose stop

# Dừng và xóa containers
docker-compose down

# Dừng và xóa cả volumes (CẢNH BÁO: mất data)
docker-compose down -v
```

### Cách 2: Chỉ chạy Backend hoặc Frontend

```bash
# Chỉ chạy backend
docker-compose up backend

# Chỉ chạy frontend (frontend cần backend)
docker-compose up frontend
```

### ✨ Training Data Auto-Load

**Docker tự động load training data lần đầu!**

Khi container khởi động:
1. Check nếu training data đã tồn tại
2. Nếu chưa có → tự động chạy `scripts/train_chinook.py`
3. Load xong thì start server

**Verify training data đã load:**
```bash
# Truy cập container
docker exec -it detomo-backend bash

# Check số lượng training items
python -c "from src.detomo_vanna import DetomoVanna; vn = DetomoVanna(config={'path': './detomo_vectordb'}); print(f'Items: {len(vn.get_training_data())}')"

# Kết quả mong đợi: Items: 93

# Thoát
exit
```

**Manual load (nếu cần):**
```bash
docker exec -it detomo-backend bash
python scripts/train_chinook.py
exit
```

---

## Chạy Local Development

**Khi nào dùng Local Development:**
- Khi muốn debug code trực tiếp
- Khi thay đổi code nhiều và muốn hot-reload nhanh
- Khi không muốn dùng Docker

### Backend Setup

```bash
# 1. Navigate to backend folder
cd backend

# 2. Create virtual environment
python3 -m venv .venv

# 3. Activate virtual environment
# macOS/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment variables
cp .env.example .env
# Sửa .env file:
# - Thêm ANTHROPIC_API_KEY=sk-ant-your-key
# - Kiểm tra các settings khác

# 6. 🔴 QUAN TRỌNG: Load training data (bắt buộc lần đầu)
python scripts/train_chinook.py
# ⚠️ Local development KHÔNG tự động load, phải chạy manual!

# 7. Start backend server
python main.py

# Hoặc với uvicorn (auto-reload):
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend chạy tại:** http://localhost:8000

**Test backend:**
```bash
# Health check
curl http://localhost:8000/api/v0/health

# API Docs (Swagger)
# Mở browser: http://localhost:8000/docs
```

### Frontend Setup (Terminal mới)

```bash
# 1. Navigate to frontend folder
cd frontend

# 2. Install dependencies (lần đầu)
npm install

# 3. Start development server
npm run dev

# Server sẽ tự động mở browser tại http://localhost:5173
```

**Frontend chạy tại:** http://localhost:5173

**Kết nối Frontend với Backend:**
- Frontend tự động kết nối với backend tại `http://localhost:8000`
- Cấu hình trong file `frontend/vite.config.ts` (proxy)

---

## Cấu trúc dự án

```
SQL-Agent/
├── backend/                    # FastAPI Backend
│   ├── app/                   # Clean Architecture
│   │   ├── main.py           # FastAPI app
│   │   ├── routers/          # API endpoints
│   │   ├── services/         # Business logic
│   │   ├── models/           # Pydantic models
│   │   ├── core/             # Config, security
│   │   └── db/               # Database
│   ├── src/                   # Legacy modules
│   │   ├── detomo_vanna.py   # Vanna integration
│   │   └── cache.py          # Cache system
│   ├── tests/                 # Tests (160+ tests)
│   ├── scripts/               # Utility scripts
│   ├── training_data/         # Training examples
│   ├── data/                  # Chinook database
│   ├── main.py               # Entry point
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile            # Production image
│   └── Dockerfile.dev        # Development image
│
├── frontend/                  # Vue3 Frontend
│   ├── src/
│   │   ├── views/            # Page components
│   │   ├── components/       # Reusable components
│   │   ├── stores/           # Pinia stores
│   │   ├── router/           # Vue Router
│   │   ├── api/              # API clients
│   │   ├── composables/      # Vue composables
│   │   ├── locales/          # i18n translations
│   │   └── types/            # TypeScript types
│   ├── public/               # Static assets
│   ├── package.json          # Node dependencies
│   ├── vite.config.ts        # Vite config
│   ├── Dockerfile            # Production image
│   └── Dockerfile.dev        # Development image
│
├── docker-compose.yml         # Development setup
├── docker-compose.prod.yml    # Production setup
└── README.md
```

---

## Lệnh thường dùng

### Docker Commands

```bash
# Build lại images
docker-compose build

# Build không dùng cache
docker-compose build --no-cache

# Restart một service cụ thể
docker-compose restart backend
docker-compose restart frontend

# Xem trạng thái containers
docker-compose ps

# Exec vào container
docker exec -it detomo-backend bash
docker exec -it detomo-frontend sh

# Xóa tất cả containers và volumes
docker-compose down -v

# Xem resource usage
docker stats
```

### Backend Commands

```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install new package
pip install <package-name>
pip freeze > requirements.txt  # Update requirements

# Run tests
PYTHONPATH=. pytest                    # All tests
PYTHONPATH=. pytest tests/unit         # Unit tests only
PYTHONPATH=. pytest --cov=app          # With coverage

# Run specific test file
PYTHONPATH=. pytest tests/unit/test_cache.py

# Format code
black .
isort .

# Type checking
mypy app/
```

### Frontend Commands

```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Linting
npm run lint

# Type checking
npm run type-check

# Unit tests
npm run test              # Watch mode
npm run test:run          # Single run
npm run test:coverage     # With coverage

# E2E tests
npm run test:e2e          # All browsers
npm run test:e2e:chromium # Chrome only
```

---

## Troubleshooting

### Backend Issues

**Problem: ModuleNotFoundError**
```bash
# Solution: Activate virtual environment
source .venv/bin/activate

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Problem: ANTHROPIC_API_KEY not set**
```bash
# Solution: Check .env file exists
ls -la .env

# Verify key is set
cat .env | grep ANTHROPIC_API_KEY
```

**Problem: Port 8000 already in use**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process (macOS/Linux)
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill

# Change port in .env
SERVER_PORT=8001
```

### Frontend Issues

**Problem: Node version too old**
```bash
# Check version
node --version  # Should be 20+

# Install Node 20 with nvm
nvm install 20
nvm use 20
```

**Problem: npm install fails**
```bash
# Clear cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

**Problem: Port 5173 already in use**
```bash
# Kill process on port 5173
lsof -i :5173 | grep LISTEN | awk '{print $2}' | xargs kill

# Or change port in vite.config.ts
server: { port: 5174 }
```

### Docker Issues

**Problem: Docker daemon not running**
```bash
# macOS: Start Docker Desktop app

# Linux: Start docker service
sudo systemctl start docker
```

**Problem: Permission denied**
```bash
# Add user to docker group (Linux)
sudo usermod -aG docker $USER
# Then logout and login again
```

**Problem: Out of memory during build**
```bash
# Increase Docker memory limit
# Docker Desktop > Settings > Resources > Memory > 8GB
```

**Problem: Container unhealthy**
```bash
# Check logs
docker logs detomo-backend
docker logs detomo-frontend

# Check health
docker inspect detomo-backend | grep Health -A 10
```

---

## Testing

### Run All Tests

```bash
# Backend tests
cd backend
PYTHONPATH=. pytest

# Frontend tests
cd frontend
npm run test:run

# E2E tests (requires both backend and frontend running)
cd frontend
npm run test:e2e
```

### Test Coverage

```bash
# Backend coverage
cd backend
PYTHONPATH=. pytest --cov=app --cov-report=html
# Open htmlcov/index.html

# Frontend coverage
cd frontend
npm run test:coverage
# Open coverage/index.html
```

---

## Production Deployment

Xem chi tiết tại: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

**Quick start:**
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start production
docker-compose -f docker-compose.prod.yml up -d

# Access
# Frontend: http://localhost
# Backend: http://localhost:8000
```

---

**Happy Coding! 🚀**
