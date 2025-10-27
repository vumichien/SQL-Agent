# Quick Start Guide - Detomo SQL AI

**Hướng dẫn nhanh để chạy ứng dụng trong 5 phút**

---

## 🚀 Cách nhanh nhất: Docker Compose

### Bước 1: Chuẩn bị

```bash
# Clone repository
git clone <repo-url>
cd SQL-Agent

# Configure API key
cd backend
cp .env.example .env
nano .env  # Thêm ANTHROPIC_API_KEY của bạn
cd ..
```

### Bước 2: Chạy

```bash
# Start tất cả (Backend + Frontend)
docker-compose up
```

**Đợi khoảng 1-2 phút để containers khởi động...**

**✨ Training data sẽ tự động load lần đầu! Không cần chạy manual.**

### Bước 3: Truy cập

- **Frontend (Vue3 UI)**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

**Done! Bây giờ bạn có thể dùng ứng dụng ngay!**

---

## 💻 Local Development (Không dùng Docker)

### Terminal 1 - Backend

```bash
cd backend

# Setup (chỉ lần đầu)
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
nano .env  # Add ANTHROPIC_API_KEY

# 🔴 Load training data (BẮT BUỘC lần đầu - không tự động)
python scripts/train_chinook.py

# Start server
python main.py
```

**Backend: http://localhost:8000**

### Terminal 2 - Frontend

```bash
cd frontend

# Setup (chỉ lần đầu)
npm install

# Start server
npm run dev
```

**Frontend: http://localhost:5173**

---

## 📝 Test thử

### Web UI
1. Mở http://localhost:5173
2. Đăng ký tài khoản mới (Register)
3. Đăng nhập
4. Gõ câu hỏi: "How many customers are there?"
5. Xem SQL được tạo tự động + kết quả + biểu đồ

### API
```bash
curl -X POST http://localhost:8000/api/v0/query \
  -H "Content-Type: application/json" \
  -d '{"question": "List top 5 customers by total spending"}'
```

---

## 🛑 Dừng ứng dụng

### Docker Compose
```bash
docker-compose down
```

### Local Development
- Nhấn `Ctrl+C` ở cả 2 terminals (backend và frontend)

---

## 🔧 Troubleshooting

**Backend không start:**
- Kiểm tra `.env` file có ANTHROPIC_API_KEY chưa
- Kiểm tra port 8000 có bị dùng không: `lsof -i :8000`

**Frontend không start:**
- Kiểm tra Node.js version ≥ 20: `node --version`
- Clear cache: `rm -rf node_modules && npm install`

**Docker lỗi:**
- Kiểm tra Docker Desktop đang chạy
- Xóa containers cũ: `docker-compose down -v`
- Build lại: `docker-compose build --no-cache`

---

## 📚 Hướng dẫn chi tiết

- **Development Guide**: [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)
- **Deployment Guide**: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- **API Documentation**: [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)
- **Full README**: [README.md](README.md)

---

**Có vấn đề? Kiểm tra [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) phần Troubleshooting**
