# Auto-Load Training Data Summary

**Tổng quan về tự động load training data**

---

## ✨ Tính năng Auto-Load

### Docker Deployment
**✅ TỰ ĐỘNG LOAD** - Không cần thao tác gì!

Khi chạy với Docker (development hoặc production):
- Container tự động kiểm tra training data khi khởi động
- Nếu chưa có data → tự động chạy `scripts/train_chinook.py`
- Nếu đã có data → skip và start server luôn

### Local Development
**❌ KHÔNG TỰ ĐỘNG** - Phải chạy manual!

Khi chạy local (không dùng Docker):
- Phải tự chạy `python scripts/train_chinook.py`
- Chỉ cần chạy 1 lần duy nhất (lần đầu)
- Lần sau không cần chạy lại (data đã có)

---

## 🔧 Cách hoạt động

### Entrypoint Script

File: `backend/docker-entrypoint.sh`

```bash
#!/bin/bash
# Docker entrypoint script

# 1. Check training data
TRAINING_COUNT=$(python -c "
from src.detomo_vanna import DetomoVanna
vn = DetomoVanna(config={'path': './detomo_vectordb'})
print(len(vn.get_training_data()))
")

# 2. Load if empty
if [ "$TRAINING_COUNT" = "0" ]; then
    echo "Loading training data..."
    python scripts/train_chinook.py
fi

# 3. Start server
exec "$@"
```

### Docker Integration

**Development (Dockerfile.dev):**
```dockerfile
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--reload"]
```

**Production (Dockerfile):**
```dockerfile
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--workers", "4"]
```

**Volume Persistence:**
```yaml
# docker-compose.yml
volumes:
  - detomo-vectordb:/app/detomo_vectordb
```
→ Data được lưu trong Docker volume, không mất khi restart

---

## 📊 So sánh

| Feature | Docker | Local |
|---------|--------|-------|
| Auto-load training data | ✅ Có | ❌ Không |
| Cần chạy manual | ❌ Không | ✅ Có |
| Lần đầu setup | Đơn giản | Thêm 1 bước |
| Data persistence | Volume | Folder |
| Startup time (lần đầu) | ~30-40s | ~10-20s |
| Startup time (lần sau) | ~10s | ~5s |

---

## 🚀 Quick Start Examples

### ✅ Docker (Tự động)

```bash
# Chỉ cần 2 bước!
cp backend/.env.example backend/.env  # Add API key
docker-compose up

# Done! Training data tự động load
```

**Console output:**
```
========================================
Detomo SQL AI Backend - Starting
========================================
Checking training data...
Current training items: 0
========================================
Training data not found. Loading...
========================================
Loading DDL files...
Loading documentation...
Loading Q&A pairs...
✓ Training data loaded successfully
========================================
Starting server...
========================================
INFO:     Application startup complete.
```

### ❌ Local (Manual)

```bash
# 3 bước bắt buộc
cd backend
source .venv/bin/activate
cp .env.example .env  # Add API key

# 🔴 Phải chạy manual!
python scripts/train_chinook.py

# Sau đó mới start
python main.py
```

---

## 🔍 Verify Training Data

### Check nếu data đã load

```bash
# Docker
docker exec -it detomo-backend bash
python -c "from src.detomo_vanna import DetomoVanna; vn = DetomoVanna(config={'path': './detomo_vectordb'}); print(f'Items: {len(vn.get_training_data())}')"

# Local
cd backend
source .venv/bin/activate
python -c "from src.detomo_vanna import DetomoVanna; vn = DetomoVanna(config={'path': './detomo_vectordb'}); print(f'Items: {len(vn.get_training_data())}')"

# Kết quả mong đợi: Items: 93
```

### Re-load training data

```bash
# Docker
docker exec -it detomo-backend bash
python scripts/train_chinook.py

# Local
cd backend
source .venv/bin/activate
python scripts/train_chinook.py
```

---

## 💡 Best Practices

### Recommendation

**✅ Dùng Docker cho development và production**
- Auto-load tiện lợi
- Consistent environment
- Không quên load data
- Volume persistence

**❌ Chỉ dùng Local khi:**
- Debug code chi tiết
- Cần control từng bước
- Không muốn dùng Docker

### Data Persistence

**Docker:**
```bash
# Data trong volume, không mất khi restart
docker volume ls | grep detomo

# Backup volume
docker run --rm -v detomo-vectordb-dev:/source -v $(pwd):/backup alpine tar czf /backup/vectordb-backup.tar.gz -C /source .

# Restore volume
docker run --rm -v detomo-vectordb-dev:/target -v $(pwd):/backup alpine tar xzf /backup/vectordb-backup.tar.gz -C /target
```

**Local:**
```bash
# Data trong folder backend/detomo_vectordb
ls -la backend/detomo_vectordb

# Backup
tar czf vectordb-backup.tar.gz backend/detomo_vectordb

# Restore
tar xzf vectordb-backup.tar.gz
```

---

## 🛠️ Troubleshooting

### Docker không auto-load

**Problem:** Container starts nhưng không có training data

**Solution:**
```bash
# Check logs
docker logs detomo-backend

# Manual load
docker exec -it detomo-backend bash
python scripts/train_chinook.py
exit

# Rebuild nếu cần
docker-compose build --no-cache backend
docker-compose up
```

### Local quên load training data

**Problem:** Server starts nhưng bị lỗi khi query

**Error:**
```
ValueError: No training data found
```

**Solution:**
```bash
# Load training data
cd backend
source .venv/bin/activate
python scripts/train_chinook.py

# Restart server
python main.py
```

### Training data bị corrupt

**Solution:**
```bash
# Docker: Xóa volume và rebuild
docker-compose down -v
docker-compose up

# Local: Xóa folder và re-load
rm -rf backend/detomo_vectordb
cd backend
python scripts/train_chinook.py
```

---

## 📝 Implementation Files

Created/Modified:
1. ✅ `backend/docker-entrypoint.sh` - Auto-load script
2. ✅ `backend/Dockerfile` - Production with entrypoint
3. ✅ `backend/Dockerfile.dev` - Development with entrypoint
4. ✅ `docker-compose.yml` - Added volume for persistence
5. ✅ `docker-compose.prod.yml` - Production volumes
6. ✅ Documentation updates (README, QUICK_START, DEVELOPMENT_GUIDE)

---

**Summary:** Docker = Auto-load ✨ | Local = Manual 🔴
