# Deployment Guide - Detomo SQL AI

**Project**: Detomo SQL AI v2.0
**Last Updated**: 2025-10-26
**Version**: 2.0.0

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment](#production-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Cloud Deployment](#cloud-deployment)
6. [Configuration](#configuration)
7. [Database Setup](#database-setup)
8. [Training Data Setup](#training-data-setup)
9. [Monitoring & Logging](#monitoring--logging)
10. [Troubleshooting](#troubleshooting)
11. [Upgrade & Maintenance](#upgrade--maintenance)

---

## Prerequisites

### System Requirements

**Minimum** (Development):
- CPU: 2 cores
- RAM: 4 GB
- Disk: 10 GB
- OS: macOS, Linux, or Windows

**Recommended** (Production):
- CPU: 4+ cores
- RAM: 8+ GB
- Disk: 20+ GB (SSD recommended)
- OS: Linux (Ubuntu 22.04 LTS or similar)

### Software Requirements

- **Python**: 3.10 or higher
- **pip**: Latest version
- **Git**: For cloning repository
- **Virtual environment**: `venv` or `virtualenv`

### API Keys

- **Anthropic API Key**: Required for Claude Agent SDK
  - Sign up at: https://console.anthropic.com
  - Create API key from dashboard
  - Note: In Claude Code environment, API key is automatically available

---

## Local Development Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/detomo/sql-ai.git
cd sql-ai
```

### Step 2: Create Virtual Environment

**On macOS/Linux**:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows**:
```cmd
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Install uv (faster package installer)
pip install uv

# Install project dependencies
uv pip install -r requirements.txt
```

**Dependencies installed**:
- FastAPI & uvicorn (web server)
- Vanna AI (Text-to-SQL framework)
- Claude Agent SDK (LLM client)
- ChromaDB (vector database)
- pandas, plotly (data processing & visualization)
- pytest (testing)

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy example file
cp .env.example .env

# Edit .env
nano .env
```

**`.env` file contents**:
```bash
# Anthropic API (for Claude Agent SDK)
ANTHROPIC_API_KEY=sk-ant-your-api-key-here

# Claude Agent SDK endpoint (internal)
CLAUDE_AGENT_ENDPOINT=http://localhost:8000/generate

# Database
DATABASE_PATH=data/chinook.db

# Vector Database (ChromaDB)
VECTOR_DB_PATH=./detomo_vectordb

# Server configuration
SERVER_HOST=localhost
SERVER_PORT=8000
LOG_LEVEL=info

# Optional: Model configuration
CLAUDE_MODEL=claude-sonnet-4-5
CLAUDE_TEMPERATURE=0.1
CLAUDE_MAX_TOKENS=2048
```

**Important**: Never commit `.env` to version control!

### Step 5: Download Database

Download the Chinook SQLite database:

```bash
# Create data directory
mkdir -p data

# Download Chinook database
curl -o data/chinook.db https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite

# Verify download
ls -lh data/chinook.db
```

### Step 6: Load Training Data

```bash
# Run training script
python scripts/train_chinook.py
```

**Expected output**:
```
Loading DDL files...
Loaded 12 DDL files
Loading documentation files...
Loaded 11 documentation files
Loading Q&A pairs...
Loaded 70 Q&A pairs
Total training data loaded: 93 items
Training complete!
```

### Step 7: Start Server

```bash
# Start FastAPI server
python claude_agent_server.py
```

**Expected output**:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Claude Agent SDK server starting...
INFO:     Using Claude Code authentication
INFO:     Initializing DetomoVanna...
INFO:     ✓ DetomoVanna initialized with 93 training items
INFO:     API documentation available at http://localhost:8000/docs
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:8000 (Press CTRL+C to quit)
```

### Step 8: Verify Installation

Open your browser to:

**Web UI**: http://localhost:8000
**API Docs**: http://localhost:8000/docs
**Health Check**: http://localhost:8000/api/v0/health

Or use curl:

```bash
# Check health
curl http://localhost:8000/api/v0/health

# Try a query
curl -X POST http://localhost:8000/api/v0/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How many customers are there?"}'
```

**Success!** You now have Detomo SQL AI running locally.

---

## Production Deployment

### Overview

Production deployment requires:
1. Process management (systemd, supervisor, or PM2)
2. Reverse proxy (nginx)
3. SSL/TLS certificates (Let's Encrypt)
4. Firewall configuration
5. Monitoring and logging
6. Automated backups

### Step 1: Server Setup

**Ubuntu 22.04 LTS** (recommended):

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.10 python3.10-venv python3-pip nginx certbot python3-certbot-nginx

# Create application user
sudo useradd -m -s /bin/bash detomo
sudo su - detomo
```

### Step 2: Deploy Application

```bash
# Clone repository
cd /home/detomo
git clone https://github.com/detomo/sql-ai.git
cd sql-ai

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install uv
uv pip install -r requirements.txt

# Download database
mkdir -p data
wget -O data/chinook.db https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite

# Configure environment
cp .env.example .env
nano .env  # Add production values

# Load training data
python scripts/train_chinook.py

# Exit detomo user
exit
```

### Step 3: Configure systemd Service

Create systemd service file:

```bash
sudo nano /etc/systemd/system/detomo-sql-ai.service
```

**Service file contents**:
```ini
[Unit]
Description=Detomo SQL AI FastAPI Server
After=network.target

[Service]
Type=simple
User=detomo
Group=detomo
WorkingDirectory=/home/detomo/sql-ai
Environment="PATH=/home/detomo/sql-ai/.venv/bin"
Environment="ANTHROPIC_API_KEY=sk-ant-your-api-key"
ExecStart=/home/detomo/sql-ai/.venv/bin/uvicorn claude_agent_server:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start service**:
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable detomo-sql-ai

# Start service
sudo systemctl start detomo-sql-ai

# Check status
sudo systemctl status detomo-sql-ai

# View logs
sudo journalctl -u detomo-sql-ai -f
```

### Step 4: Configure nginx Reverse Proxy

Create nginx configuration:

```bash
sudo nano /etc/nginx/sites-available/detomo-sql-ai
```

**nginx configuration**:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # Redirect HTTP to HTTPS (after SSL setup)
    # return 301 https://$server_name$request_uri;

    # Proxy to FastAPI
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support (if needed in future)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Timeouts (for long-running queries)
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Increase max body size (for large training data uploads)
    client_max_body_size 10M;

    # Logging
    access_log /var/log/nginx/detomo_access.log;
    error_log /var/log/nginx/detomo_error.log;
}
```

**Enable site**:
```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/detomo-sql-ai /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### Step 5: Configure SSL/TLS with Let's Encrypt

```bash
# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Follow prompts:
# - Enter email
# - Agree to terms
# - Choose redirect HTTP to HTTPS (option 2)

# Verify auto-renewal
sudo certbot renew --dry-run
```

**nginx automatically updated with SSL**:
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # ... rest of configuration
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

### Step 6: Configure Firewall

```bash
# Enable UFW firewall
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Block direct access to port 8000
# (nginx proxies to it, no need for external access)

# Check status
sudo ufw status
```

### Step 7: Verify Production Deployment

```bash
# Check service status
sudo systemctl status detomo-sql-ai

# Check nginx status
sudo systemctl status nginx

# Test health endpoint
curl https://your-domain.com/api/v0/health

# Test query
curl -X POST https://your-domain.com/api/v0/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How many customers are there?"}'
```

**Success!** Your production deployment is complete.

---

## Docker Deployment

### Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir uv && \
    uv pip install --system --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Download Chinook database
RUN mkdir -p data && \
    curl -o data/chinook.db https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite

# Create volume for ChromaDB
VOLUME /app/detomo_vectordb

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run training script on first start, then start server
CMD python scripts/train_chinook.py && \
    uvicorn claude_agent_server:app --host 0.0.0.0 --port 8000 --workers 4
```

### docker-compose.yml

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  detomo-sql-ai:
    build: .
    container_name: detomo-sql-ai
    ports:
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - DATABASE_PATH=data/chinook.db
      - VECTOR_DB_PATH=./detomo_vectordb
      - LOG_LEVEL=info
    volumes:
      - ./detomo_vectordb:/app/detomo_vectordb
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  # Optional: nginx reverse proxy
  nginx:
    image: nginx:alpine
    container_name: detomo-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - detomo-sql-ai
    restart: unless-stopped
```

### Build and Run

```bash
# Build image
docker build -t detomo-sql-ai:latest .

# Run container
docker run -d \
  --name detomo-sql-ai \
  -p 8000:8000 \
  -e ANTHROPIC_API_KEY=sk-ant-your-key \
  -v $(pwd)/detomo_vectordb:/app/detomo_vectordb \
  detomo-sql-ai:latest

# Or use docker-compose
docker-compose up -d

# View logs
docker logs -f detomo-sql-ai

# Check status
docker ps

# Stop container
docker stop detomo-sql-ai

# Remove container
docker rm detomo-sql-ai
```

---

## Cloud Deployment

### AWS Deployment (Elastic Beanstalk)

**Step 1: Install EB CLI**
```bash
pip install awsebcli
```

**Step 2: Initialize EB Application**
```bash
eb init -p python-3.10 detomo-sql-ai --region us-east-1
```

**Step 3: Create Environment**
```bash
eb create detomo-sql-ai-prod \
  --envvars ANTHROPIC_API_KEY=sk-ant-your-key
```

**Step 4: Deploy**
```bash
eb deploy
```

**Step 5: Open Application**
```bash
eb open
```

### Google Cloud Run

**Step 1: Build and Push Image**
```bash
# Configure project
gcloud config set project YOUR_PROJECT_ID

# Build image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/detomo-sql-ai

# Deploy to Cloud Run
gcloud run deploy detomo-sql-ai \
  --image gcr.io/YOUR_PROJECT_ID/detomo-sql-ai \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY=sk-ant-your-key \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300s \
  --max-instances 10
```

### Azure Container Instances

**Step 1: Login to Azure**
```bash
az login
```

**Step 2: Create Resource Group**
```bash
az group create --name detomo-rg --location eastus
```

**Step 3: Deploy Container**
```bash
az container create \
  --resource-group detomo-rg \
  --name detomo-sql-ai \
  --image your-registry/detomo-sql-ai:latest \
  --dns-name-label detomo-sql-ai \
  --ports 8000 \
  --environment-variables ANTHROPIC_API_KEY=sk-ant-your-key \
  --cpu 2 \
  --memory 4
```

### Heroku

**Step 1: Create Heroku App**
```bash
heroku create detomo-sql-ai
```

**Step 2: Set Environment Variables**
```bash
heroku config:set ANTHROPIC_API_KEY=sk-ant-your-key
```

**Step 3: Create Procfile**
```bash
echo "web: uvicorn claude_agent_server:app --host 0.0.0.0 --port \$PORT" > Procfile
```

**Step 4: Deploy**
```bash
git push heroku main
```

---

## Configuration

### Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | Yes | - | Anthropic API key for Claude |
| `DATABASE_PATH` | No | `data/chinook.db` | Path to SQLite database |
| `VECTOR_DB_PATH` | No | `./detomo_vectordb` | ChromaDB storage path |
| `CLAUDE_MODEL` | No | `claude-sonnet-4-5` | Claude model to use |
| `CLAUDE_TEMPERATURE` | No | `0.1` | LLM temperature (0.0-1.0) |
| `CLAUDE_MAX_TOKENS` | No | `2048` | Max tokens per response |
| `SERVER_HOST` | No | `localhost` | Server bind address |
| `SERVER_PORT` | No | `8000` | Server port |
| `LOG_LEVEL` | No | `info` | Log level (debug/info/warning/error) |

### Performance Tuning

**uvicorn workers** (production):
```bash
# Auto-detect number of CPUs
uvicorn claude_agent_server:app --workers $(nproc)

# Or specify manually
uvicorn claude_agent_server:app --workers 4
```

**Memory considerations**:
- Base memory: ~200 MB
- Per worker: ~100-200 MB
- ChromaDB: ~50-100 MB
- Total recommended: 1 GB + (workers × 200 MB)

**Example**: 4 workers = 1 GB + 800 MB = 1.8 GB minimum

---

## Database Setup

### Using Different Databases

Detomo SQL AI supports any database that Vanna supports.

#### PostgreSQL

```python
# In claude_agent_server.py, replace:
vn.connect_to_sqlite("data/chinook.db")

# With:
vn.connect_to_postgres(
    host="localhost",
    dbname="chinook",
    user="postgres",
    password="your-password",
    port=5432
)
```

#### MySQL

```python
vn.connect_to_mysql(
    host="localhost",
    dbname="chinook",
    user="root",
    password="your-password",
    port=3306
)
```

#### Snowflake

```python
vn.connect_to_snowflake(
    account="your-account",
    username="your-username",
    password="your-password",
    database="CHINOOK",
    schema="PUBLIC"
)
```

### Database Migrations

If you're connecting to a custom database:

1. Export your schema:
```bash
# PostgreSQL
pg_dump -s dbname > schema.sql

# MySQL
mysqldump --no-data dbname > schema.sql
```

2. Add DDL to training data:
```bash
# Place in training_data/your_db/ddl/
cp schema.sql training_data/your_db/ddl/
```

3. Re-run training script:
```bash
python scripts/train_chinook.py
```

---

## Training Data Setup

### Adding Custom Training Data

Create training data structure:

```
training_data/
└── your_database/
    ├── ddl/
    │   └── tables.sql
    ├── documentation/
    │   └── table_docs.md
    └── questions/
        └── qa_pairs.json
```

**DDL Example** (`ddl/tables.sql`):
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT UNIQUE,
    created_at TIMESTAMP
);
```

**Documentation Example** (`documentation/users.md`):
```markdown
# Users Table

Stores user account information.

## Columns
- user_id: Unique user identifier
- username: User's display name
- email: User's email address (unique)
- created_at: Account creation timestamp
```

**Q&A Example** (`questions/user_queries.json`):
```json
[
  {
    "question": "How many users are there?",
    "sql": "SELECT COUNT(*) FROM users"
  },
  {
    "question": "List the 10 most recent users",
    "sql": "SELECT * FROM users ORDER BY created_at DESC LIMIT 10"
  }
]
```

### Training Script

Modify `scripts/train_chinook.py` to load your data:

```python
# Add to training script
vn.train(ddl=open("training_data/your_database/ddl/tables.sql").read())
vn.train(documentation=open("training_data/your_database/documentation/users.md").read())

# Load Q&A pairs
import json
qa_data = json.load(open("training_data/your_database/questions/user_queries.json"))
for item in qa_data:
    vn.train(question=item["question"], sql=item["sql"])
```

---

## Monitoring & Logging

### Application Logs

**View logs** (systemd):
```bash
# Follow logs
sudo journalctl -u detomo-sql-ai -f

# Last 100 lines
sudo journalctl -u detomo-sql-ai -n 100

# Logs from today
sudo journalctl -u detomo-sql-ai --since today

# Logs with errors only
sudo journalctl -u detomo-sql-ai -p err
```

**Log levels**:
- `DEBUG`: Detailed debugging information
- `INFO`: General informational messages (default)
- `WARNING`: Warning messages
- `ERROR`: Error messages
- `CRITICAL`: Critical errors

**Change log level**:
```bash
# In .env file
LOG_LEVEL=debug
```

### Health Monitoring

**Endpoint**: `GET /api/v0/health`

**Response**:
```json
{
  "status": "healthy",
  "service": "Detomo SQL AI API",
  "version": "2.0.0",
  "llm_endpoint": "http://localhost:8000/generate",
  "database": "data/chinook.db - Connected",
  "training_data_count": 93
}
```

**Setup monitoring** (cron job):
```bash
# Check health every 5 minutes
*/5 * * * * curl -f http://localhost:8000/api/v0/health || echo "Health check failed" | mail -s "Detomo SQL AI Alert" admin@example.com
```

### Performance Monitoring

Use tools like:
- **Prometheus + Grafana**: Metrics and dashboards
- **Datadog**: Full-stack monitoring
- **New Relic**: APM and infrastructure
- **Sentry**: Error tracking

---

## Troubleshooting

### Common Issues

#### 1. Port Already in Use

**Error**: `[Errno 48] Address already in use`

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change port
uvicorn claude_agent_server:app --port 8001
```

#### 2. ChromaDB Lock Error

**Error**: `Database is locked`

**Solution**:
```bash
# Stop all processes
sudo systemctl stop detomo-sql-ai

# Remove lock file
rm detomo_vectordb/chroma.sqlite3-wal

# Restart
sudo systemctl start detomo-sql-ai
```

#### 3. API Key Not Found

**Error**: `AuthenticationError: Invalid API key`

**Solution**:
```bash
# Check .env file
cat .env | grep ANTHROPIC_API_KEY

# Ensure key is loaded
export ANTHROPIC_API_KEY=sk-ant-your-key

# Or set in systemd service
sudo nano /etc/systemd/system/detomo-sql-ai.service
# Add: Environment="ANTHROPIC_API_KEY=sk-ant-your-key"

sudo systemctl daemon-reload
sudo systemctl restart detomo-sql-ai
```

#### 4. Module Not Found

**Error**: `ModuleNotFoundError: No module named 'vanna'`

**Solution**:
```bash
# Activate virtual environment
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep vanna
```

#### 5. Database Not Found

**Error**: `unable to open database file`

**Solution**:
```bash
# Check database exists
ls -lh data/chinook.db

# Download if missing
curl -o data/chinook.db https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite

# Check permissions
chmod 644 data/chinook.db
```

---

## Upgrade & Maintenance

### Upgrading Application

```bash
# Stop service
sudo systemctl stop detomo-sql-ai

# Backup current version
cd /home/detomo
cp -r sql-ai sql-ai.backup

# Pull latest code
cd sql-ai
git pull origin main

# Update dependencies
source .venv/bin/activate
pip install -r requirements.txt

# Run migrations (if any)
# python scripts/migrate.py

# Restart service
sudo systemctl start detomo-sql-ai

# Check status
sudo systemctl status detomo-sql-ai
```

### Backup Strategy

**1. Backup ChromaDB**:
```bash
# Daily backup (cron job)
0 2 * * * tar -czf /backups/detomo_vectordb_$(date +\%Y\%m\%d).tar.gz /home/detomo/sql-ai/detomo_vectordb
```

**2. Backup Database**:
```bash
# SQLite backup
cp data/chinook.db data/chinook.db.backup

# PostgreSQL backup
pg_dump dbname > backup.sql
```

**3. Backup Configuration**:
```bash
# Backup .env file
cp .env .env.backup
```

### Database Maintenance

**Vacuum ChromaDB**:
```bash
# Stop service
sudo systemctl stop detomo-sql-ai

# Vacuum database
sqlite3 detomo_vectordb/chroma.sqlite3 "VACUUM;"

# Restart service
sudo systemctl start detomo-sql-ai
```

**Clear cache** (if needed):
```bash
# Cache is in-memory, so restart clears it
sudo systemctl restart detomo-sql-ai
```

---

## Security Checklist

- [ ] Use strong API keys (rotate regularly)
- [ ] Enable HTTPS with valid SSL certificates
- [ ] Configure firewall (block unnecessary ports)
- [ ] Use environment variables (never hardcode secrets)
- [ ] Implement rate limiting (production)
- [ ] Enable authentication (production)
- [ ] Regular security updates (`apt upgrade`)
- [ ] Monitor logs for suspicious activity
- [ ] Use read-only database user (if possible)
- [ ] Backup data regularly
- [ ] Implement intrusion detection (fail2ban)

---

## Support

For deployment issues or questions:
- **GitHub Issues**: [github.com/detomo/sql-ai/issues](https://github.com/detomo/sql-ai/issues)
- **Documentation**: [docs.detomo.com](https://docs.detomo.com)
- **Email**: support@detomo.com

---

**Document Version**: 1.0
**Last Updated**: 2025-10-26
**Tested On**: Ubuntu 22.04 LTS, macOS 13+, Windows 11
