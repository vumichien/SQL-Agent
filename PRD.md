# PRD: Detomo SQL AI

**Product Requirements Document**
**Version:** 1.0
**Date:** 2025-10-25
**Author:** Detomo Team
**Status:** Draft

---

## 1. EXECUTIVE SUMMARY

### 1.1 Product Overview
Detomo SQL AI is an AI-powered Text-to-SQL application that allows users to query databases using natural language (Japanese/English), automatically generates SQL queries, and displays results visually.

### 1.2 Technology Stack
- **Backend LLM**: Claude Agent SDK (Anthropic)
- **RAG Framework**: Vanna AI
- **Vector Database**: ChromaDB (dev) / PGVector (production)
- **Embedding Model**: BAAI/bge-m3 (HuggingFace)
- **Target Database**: PostgreSQL (Chinook sample database)
- **Frontend**: Vanna-Flask (customized)
- **Language**: Python 3.10+

### 1.3 Core Features
- Natural language to SQL conversion
- Auto-generated visualizations (charts/graphs)
- Training data management (DDL, Documentation, Q&A pairs)
- Interactive chat interface
- Multi-turn conversation support
- Japanese & English language support

---

## 2. OBJECTIVES & GOALS

### 2.1 Business Objectives
1. Democratize database access for non-technical users
2. Reduce query time from hours → minutes
3. Improve data-driven decision making
4. Showcase Detomo AI capabilities

### 2.2 Technical Goals
1. **Accuracy**: ≥ 85% SQL generation accuracy on Chinook database
2. **Performance**: Response time < 5 seconds for simple queries
3. **Scalability**: Support 100+ concurrent users
4. **Reliability**: 99% uptime

### 2.3 Success Metrics
- SQL correctness rate: ≥ 85%
- User query success rate: ≥ 90%
- Average response time: < 5s
- User satisfaction score: ≥ 4/5

---

## 3. USER STORIES

### 3.1 Primary Personas

**Persona 1: Business Analyst (Non-technical)**
- "月次売上を見たいけど、SQLを知らない" / "I want to see monthly revenue without knowing SQL"
- "売上トップ10の顧客が必要です" / "I need top 10 customers by revenue"
- "結果をExcelにエクスポートしたい" / "I want to export results to Excel"

**Persona 2: Data Analyst (Technical)**
- "実行前に生成されたSQLを検証したい" / "I want to validate generated SQL before execution"
- "ドメイン固有のクエリをトレーニングする必要がある" / "I need to train domain-specific queries"
- "視覚化スタイルをカスタマイズしたい" / "I want to customize visualization styles"

**Persona 3: Admin/Developer**
- "トレーニングデータを管理する必要がある" / "I need to manage training data"
- "クエリのパフォーマンスを監視したい" / "I want to monitor query performance"
- "権限を設定する必要がある" / "I need to configure permissions"

### 3.2 User Flows

#### Flow 1: Simple Query
```
User Input: "顧客は何人いますか？" / "How many customers are there?"
    ↓
System generates SQL: SELECT COUNT(*) FROM Customer
    ↓
Execute & return results
    ↓
Display: "59人の顧客がいます" / "There are 59 customers"
```

#### Flow 2: Complex Query with Visualization
```
User Input: "2024年のジャンル別売上" / "Revenue by genre in 2024"
    ↓
System generates SQL: SELECT g.Name, SUM(il.UnitPrice * il.Quantity) ...
    ↓
Execute & return DataFrame
    ↓
Auto-generate bar chart
    ↓
Display results + visualization
```

#### Flow 3: Training Data Management
```
Admin uploads DDL file
    ↓
System parses and trains
    ↓
Admin adds sample Q&A pairs
    ↓
System indexes to vector DB
    ↓
Ready for inference
```

---

## 4. FUNCTIONAL REQUIREMENTS

### 4.1 Backend Architecture

#### 4.1.1 LLM Integration Strategy

**Development Environment**: Claude Agent SDK (Local/Free)
**Production Environment**: Anthropic API (Cloud/Paid)

**Reason for using 2 environments**:
- **Agent SDK** (Development):
  - ✅ **FREE** - Save costs during development and testing
  - ✅ Run locally, no API key required or use free tier API key
  - ✅ Suitable for training, testing, debugging
  - ⚠️ Trade-off: More complex, requires custom wrapper

- **Anthropic API** (Production):
  - ✅ **Production-ready** - Stable, fast, reliable
  - ✅ Simple, built-in support in Vanna
  - ✅ Better performance, lower latency
  - ⚠️ Trade-off: Paid service (pay-per-token)

---

### **Development Setup (Claude Agent SDK)**

**Implementation với Custom Wrapper**:

```python
import asyncio
from typing import List, Dict, Any
from vanna.base import VannaBase
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock
from chromadb.utils import embedding_functions

class ClaudeAgentChat(VannaBase):
    """
    Custom wrapper cho Claude Agent SDK.
    Để tích hợp với Vanna framework.
    """

    def __init__(self, config=None):
        VannaBase.__init__(self, config=config)

        # Config
        self.temperature = config.get("temperature", 0.1) if config else 0.1
        self.max_tokens = config.get("max_tokens", 2048) if config else 2048
        self.model = config.get("model", "claude-3-5-sonnet-20241022") if config else "claude-3-5-sonnet-20241022"

        # Agent SDK options
        self.agent_options = ClaudeAgentOptions(
            system_prompt=None,  # Will be set per query
            permission_mode="bypassPermissions",
            max_turns=10
        )

        # Event loop for async operations
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def system_message(self, message: str) -> Dict[str, Any]:
        return {"role": "system", "content": message}

    def user_message(self, message: str) -> Dict[str, Any]:
        return {"role": "user", "content": message}

    def assistant_message(self, message: str) -> Dict[str, Any]:
        return {"role": "assistant", "content": message}

    def submit_prompt(self, prompt: List[Dict[str, Any]], **kwargs) -> str:
        """
        Vanna calls this method. We convert to Agent SDK format.
        """
        return self.loop.run_until_complete(self._async_submit_prompt(prompt, **kwargs))

    async def _async_submit_prompt(self, prompt: List[Dict[str, Any]], **kwargs) -> str:
        """
        Async implementation using Claude Agent SDK.
        """
        # Extract system message
        system_message = ""
        user_messages = []

        for msg in prompt:
            role = msg.get("role")
            content = msg.get("content", "")

            if role == "system":
                system_message = content
            elif role == "user":
                user_messages.append(content)

        # Get last user message
        last_user_msg = user_messages[-1] if user_messages else ""

        # Setup options
        options = ClaudeAgentOptions(
            system_prompt=system_message if system_message else "claude_code",
            permission_mode="bypassPermissions",
            max_turns=10
        )

        # Use Agent SDK
        async with ClaudeSDKClient(options=options) as client:
            await client.query(last_user_msg)

            # Collect response
            response_text = ""
            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            response_text += block.text

            return response_text

    def __del__(self):
        """Cleanup event loop"""
        if hasattr(self, 'loop') and self.loop.is_running():
            self.loop.close()

# Main Vanna class for Development
from vanna.chromadb import ChromaDB_VectorStore

class DetomoVannaDev(ChromaDB_VectorStore, ClaudeAgentChat):
    """Development version using Claude Agent SDK"""
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        ClaudeAgentChat.__init__(self, config=config)
```

**Usage (Development)**:
```python
# Development với Agent SDK (FREE)
vn = DetomoVannaDev(config={
    # ChromaDB
    "path": "./detomo_vectordb",
    "client": "persistent",
    "embedding_function": embedding_functions.SentenceTransformerEmbeddingFunction("BAAI/bge-m3"),

    # Claude Agent SDK (local)
    "model": "claude-3-5-sonnet-20241022",
    "temperature": 0.1,
    "max_tokens": 2048
})
```

---

### **Production Setup (Anthropic API)**

**Implementation (Simple)**:

```python
from vanna.chromadb import ChromaDB_VectorStore
from vanna.anthropic import Anthropic_Chat

class DetomoVannaProd(ChromaDB_VectorStore, Anthropic_Chat):
    """Production version using Anthropic API"""
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Anthropic_Chat.__init__(self, config=config)
```

**Usage (Production)**:
```python
# Production với Anthropic API (PAID)
vn = DetomoVannaProd(config={
    # ChromaDB
    "path": "./detomo_vectordb",
    "client": "persistent",

    # Anthropic API
    "api_key": os.getenv("ANTHROPIC_API_KEY"),
    "model": "claude-3-5-sonnet-20241022",
    "temperature": 0.1,
    "max_tokens": 2048
})
```

---

### **Migration Path**

**Step 1 - Development**: Dùng `DetomoVannaDev` (Agent SDK)
```python
from detomo_vanna import DetomoVannaDev
vn = DetomoVannaDev(config=dev_config)
```

**Step 2 - Production**: Switch to `DetomoVannaProd` (Anthropic API)
```python
from detomo_vanna import DetomoVannaProd
vn = DetomoVannaProd(config=prod_config)
```

**Both classes share**:
- Use same training data (vector DB)
- Have same interface (Vanna methods)
- Only differ in LLM backend

---

### **Configuration**

**Common Settings**:
- Model: `claude-3-5-sonnet-20241022`
- Temperature: `0.1` (deterministic SQL)
- Max Tokens: `2048`
- Embedding: `BAAI/bge-m3`

**Environment-specific**:
- **Dev**: No API key required (or free tier)
- **Prod**: `ANTHROPIC_API_KEY` required

#### 4.1.2 Vector Database Setup

**Development**: ChromaDB
```python
config = {
    "path": "./detomo_vectordb",
    "client": "persistent",
    "embedding_function": HuggingFaceEmbeddings("BAAI/bge-m3"),
    "n_results_sql": 10,
    "n_results_ddl": 10,
    "n_results_documentation": 10
}
```

**Production**: PGVector
```python
config = {
    "connection_string": "postgresql://user:pass@localhost:5432/detomo_vectors",
    "embedding_function": HuggingFaceEmbeddings("BAAI/bge-m3"),
    "n_results": 10
}
```

#### 4.1.3 Database Connection (Chinook PostgreSQL)
```python
vn.connect_to_postgres(
    host=os.getenv("DB_HOST", "localhost"),
    dbname="chinook",
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD"),
    port=5432
)
```

### 4.2 Training Data Requirements

#### 4.2.1 Chinook Database Setup

**Data Source**: https://github.com/lerocha/chinook-database

**PostgreSQL Scripts**:
1. `chinook_ddl.sql` - Tables & constraints
2. `chinook_genres_artists_albums.sql` - Artists/albums data
3. `chinook_songs.sql` - Songs data

**Schema Overview**:
```
Tables:
- Album (AlbumId, Title, ArtistId)
- Artist (ArtistId, Name)
- Customer (CustomerId, FirstName, LastName, Email, Country, etc.)
- Employee (EmployeeId, FirstName, LastName, Title, etc.)
- Genre (GenreId, Name)
- Invoice (InvoiceId, CustomerId, InvoiceDate, Total, etc.)
- InvoiceLine (InvoiceLineId, InvoiceId, TrackId, UnitPrice, Quantity)
- MediaType (MediaTypeId, Name)
- Playlist (PlaylistId, Name)
- PlaylistTrack (PlaylistId, TrackId)
- Track (TrackId, Name, AlbumId, MediaTypeId, GenreId, Composer, etc.)
```

#### 4.2.2 Training Data Structure

**Directory Structure**:
```
training_data/
├── chinook/
│   ├── ddl/
│   │   ├── album.sql
│   │   ├── artist.sql
│   │   ├── customer.sql
│   │   ├── employee.sql
│   │   ├── genre.sql
│   │   ├── invoice.sql
│   │   ├── invoice_line.sql
│   │   ├── media_type.sql
│   │   ├── playlist.sql
│   │   ├── track.sql
│   │   └── relationships.sql
│   ├── documentation/
│   │   ├── album.md
│   │   ├── artist.md
│   │   ├── customer.md
│   │   ├── invoice.md
│   │   └── business_rules.md
│   └── questions/
│       ├── basic_queries.json
│       ├── aggregation_queries.json
│       ├── join_queries.json
│       └── japanese_queries.json
```

**DDL Examples**:
```sql
-- ddl/customer.sql
CREATE TABLE Customer (
    CustomerId INTEGER PRIMARY KEY,
    FirstName VARCHAR(40) NOT NULL,
    LastName VARCHAR(20) NOT NULL,
    Email VARCHAR(60) NOT NULL,
    Country VARCHAR(40),
    State VARCHAR(40),
    City VARCHAR(40),
    Phone VARCHAR(24),
    Fax VARCHAR(24),
    SupportRepId INTEGER,
    FOREIGN KEY (SupportRepId) REFERENCES Employee(EmployeeId)
);
```

**Documentation Examples**:
```markdown
# Customer Table

## Description
The Customer table stores customer information for the digital music store.

## Columns
- **CustomerId**: Unique customer ID (Primary Key)
- **FirstName**: Customer first name
- **LastName**: Customer last name
- **Email**: Email (unique, required)
- **Country**: Country (used for regional analysis)
- **City**: City
- **SupportRepId**: Support representative ID (Foreign Key → Employee)

## Business Rules
- Email must be unique
- Each customer can have 0 or more invoices
- SupportRepId links to Employee.Title = "Sales Support Agent"
```

**Question-Answer Pairs** (`questions/basic_queries.json`):
```json
[
  {
    "question": "顧客は何人いますか？ / How many customers are there?",
    "sql": "SELECT COUNT(*) FROM Customer"
  },
  {
    "question": "最初の10人の顧客をリストしてください / List first 10 customers",
    "sql": "SELECT * FROM Customer LIMIT 10"
  },
  {
    "question": "How many customers are from USA?",
    "sql": "SELECT COUNT(*) FROM Customer WHERE Country = 'USA'"
  },
  {
    "question": "売上トップ10の顧客 / Top 10 customers by revenue",
    "sql": "SELECT c.CustomerId, c.FirstName, c.LastName, SUM(i.Total) as TotalSpent FROM Customer c JOIN Invoice i ON c.CustomerId = i.CustomerId GROUP BY c.CustomerId, c.FirstName, c.LastName ORDER BY TotalSpent DESC LIMIT 10"
  }
]
```

**Aggregation Queries** (`questions/aggregation_queries.json`):
```json
[
  {
    "question": "2024年の月別総売上 / Total revenue by month in 2024",
    "sql": "SELECT DATE_TRUNC('month', InvoiceDate) as Month, SUM(Total) as Revenue FROM Invoice WHERE EXTRACT(YEAR FROM InvoiceDate) = 2024 GROUP BY Month ORDER BY Month"
  },
  {
    "question": "国別の売上 / Revenue by country",
    "sql": "SELECT BillingCountry, SUM(Total) as Revenue FROM Invoice GROUP BY BillingCountry ORDER BY Revenue DESC"
  },
  {
    "question": "最も売れている音楽ジャンルは？ / Which music genre sells best?",
    "sql": "SELECT g.Name, COUNT(il.InvoiceLineId) as TimesSold, SUM(il.Quantity) as TotalQuantity FROM Genre g JOIN Track t ON g.GenreId = t.GenreId JOIN InvoiceLine il ON t.TrackId = il.TrackId GROUP BY g.Name ORDER BY TotalQuantity DESC LIMIT 10"
  }
]
```

**Join Queries** (`questions/join_queries.json`):
```json
[
  {
    "question": "アルバムとアーティストをリストしてください / List albums and artists",
    "sql": "SELECT al.Title as Album, ar.Name as Artist FROM Album al JOIN Artist ar ON al.ArtistId = ar.ArtistId ORDER BY ar.Name"
  },
  {
    "question": "'Music'プレイリストのトラックリスト / List of tracks in 'Music' playlist",
    "sql": "SELECT t.Name as TrackName, ar.Name as Artist, al.Title as Album FROM Playlist p JOIN PlaylistTrack pt ON p.PlaylistId = pt.PlaylistId JOIN Track t ON pt.TrackId = t.TrackId JOIN Album al ON t.AlbumId = al.AlbumId JOIN Artist ar ON al.ArtistId = ar.ArtistId WHERE p.Name = 'Music'"
  }
]
```

#### 4.2.3 Training Script

**File**: `scripts/train_chinook.py`

```python
import os
import json
from pathlib import Path
from detomo_vanna import DetomoVanna

def load_training_data():
    """Load all training data from files"""

    vn = DetomoVanna(config={
        "path": "./detomo_vectordb",
        "client": "persistent",
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.1,
        "max_tokens": 2048
    })

    vn.connect_to_postgres(
        host="localhost",
        dbname="chinook",
        user="postgres",
        password=os.getenv("DB_PASSWORD")
    )

    # 1. Train DDL
    print("Training DDL...")
    ddl_dir = Path("training_data/chinook/ddl")
    for ddl_file in ddl_dir.glob("*.sql"):
        with open(ddl_file, 'r', encoding='utf-8') as f:
            ddl_content = f.read()
            vn.train(ddl=ddl_content)
            print(f"✓ Trained {ddl_file.name}")

    # 2. Train Documentation
    print("\nTraining Documentation...")
    doc_dir = Path("training_data/chinook/documentation")
    for doc_file in doc_dir.glob("*.md"):
        with open(doc_file, 'r', encoding='utf-8') as f:
            doc_content = f.read()
            vn.train(documentation=doc_content)
            print(f"✓ Trained {doc_file.name}")

    # 3. Train Q&A Pairs
    print("\nTraining Questions...")
    qa_dir = Path("training_data/chinook/questions")
    for qa_file in qa_dir.glob("*.json"):
        with open(qa_file, 'r', encoding='utf-8') as f:
            qa_pairs = json.load(f)
            for pair in qa_pairs:
                vn.train(
                    question=pair["question"],
                    sql=pair["sql"]
                )
            print(f"✓ Trained {len(qa_pairs)} pairs from {qa_file.name}")

    print("\n✅ Training completed!")

    # Verify training data
    df = vn.get_training_data()
    print(f"\nTotal training items: {len(df)}")
    print(f"- DDL: {len(df[df['training_data_type'] == 'ddl'])}")
    print(f"- Documentation: {len(df[df['training_data_type'] == 'documentation'])}")
    print(f"- Q&A: {len(df[df['training_data_type'] == 'sql'])}")

if __name__ == "__main__":
    load_training_data()
```

### 4.3 Frontend Requirements (Vanna-Flask Customization)

#### 4.3.1 Branding Changes
**Original**: Vanna AI
**New**: Detomo SQL AI

**Files to modify**:
- `static/index.html` - Update title, logo, branding
- `static/styles.css` - Update color scheme (Detomo brand colors)
- `app.py` - Update app name, metadata

#### 4.3.2 UI Components

**Required Pages**:
1. **Home/Chat Interface** (`/`)
   - Chat input box
   - Query history sidebar
   - Results display area
   - Visualization panel

2. **Training Management** (`/admin/training`)
   - Upload DDL files
   - Add Q&A pairs manually
   - View/delete training data
   - Training statistics

3. **Settings** (`/settings`)
   - Database connection config
   - Model parameters (temperature, etc.)
   - Language preference (VI/EN)

4. **Analytics Dashboard** (`/analytics`)
   - Query success rate
   - Popular queries
   - Performance metrics
   - Error logs

#### 4.3.3 Key Features

**Chat Interface**:
- Markdown support for formatted responses
- Code syntax highlighting for SQL
- Copy-to-clipboard button for SQL
- Download results as CSV/Excel
- Auto-complete suggestions

**Visualization**:
- Auto-detect chart type (bar, line, pie, scatter)
- Interactive charts (Plotly)
- Customizable colors/themes
- Export chart as PNG/SVG

**Multi-language Support**:
- Japanese UI labels
- English UI labels
- Auto-detect query language
- Bilingual documentation

#### 4.3.4 File Structure
```
detomo-sql-ai/
├── app.py                    # Main Flask app
├── detomo_vanna.py          # Custom Vanna class
├── config.py                # Configuration
├── requirements.txt         # Dependencies
├── static/
│   ├── css/
│   │   └── detomo.css      # Custom styles
│   ├── js/
│   │   ├── chat.js         # Chat logic
│   │   ├── viz.js          # Visualization
│   │   └── admin.js        # Admin panel
│   ├── images/
│   │   └── detomo-logo.png
│   └── index.html
├── templates/
│   ├── base.html
│   ├── chat.html
│   ├── admin.html
│   └── settings.html
├── scripts/
│   └── train_chinook.py    # Training script
├── training_data/
│   └── chinook/            # Training data
└── tests/
    └── test_queries.py     # Test cases
```

### 4.4 API Endpoints

#### 4.4.1 Core Endpoints

**POST /api/v0/generate_sql**
```json
Request:
{
  "question": "Top 10 customers by revenue",
  "language": "en"
}

Response:
{
  "sql": "SELECT c.FirstName, c.LastName, SUM(i.Total) ...",
  "execution_time": 1.2,
  "status": "success"
}
```

**POST /api/v0/run_sql**
```json
Request:
{
  "sql": "SELECT * FROM Customer LIMIT 10"
}

Response:
{
  "df": [...],  // JSON serialized DataFrame
  "columns": ["CustomerId", "FirstName", ...],
  "rows": 10,
  "execution_time": 0.5
}
```

**POST /api/v0/generate_plotly_figure**
```json
Request:
{
  "question": "Revenue by country",
  "sql": "SELECT Country, SUM(Total) ...",
  "df": [...]
}

Response:
{
  "plotly_json": {...},
  "chart_type": "bar"
}
```

**GET /api/v0/get_training_data**
```json
Response:
{
  "data": [
    {
      "id": "abc-123-sql",
      "type": "sql",
      "question": "...",
      "content": "SELECT ..."
    }
  ],
  "total": 150
}
```

**POST /api/v0/train**
```json
Request:
{
  "type": "sql",  // or "ddl", "documentation"
  "question": "How many customers?",
  "sql": "SELECT COUNT(*) FROM Customer"
}

Response:
{
  "id": "xyz-456-sql",
  "status": "success"
}
```

**DELETE /api/v0/remove_training_data**
```json
Request:
{
  "id": "xyz-456-sql"
}

Response:
{
  "status": "success"
}
```

### 4.5 Non-Functional Requirements

#### 4.5.1 Performance
- SQL generation: < 5s (p95)
- SQL execution: < 3s (p95)
- Visualization generation: < 2s (p95)
- Page load time: < 2s

#### 4.5.2 Security
- SQL injection prevention (parameterized queries)
- Rate limiting (10 requests/minute per user)
- API key authentication
- Read-only database user for queries
- HTTPS only in production

#### 4.5.3 Scalability
- Support 100 concurrent users
- Horizontal scaling via Docker/K8s
- Vector DB caching
- LLM response caching

#### 4.5.4 Reliability
- Error handling for invalid SQL
- Graceful degradation if LLM unavailable
- Retry logic (3 attempts)
- Logging & monitoring
- 99% uptime SLA

---

## 5. TECHNICAL SPECIFICATIONS

### 5.1 Dependencies

**Core**:
```
vanna==0.7.9
anthropic>=0.40.0
chromadb<1.0.0
psycopg2-binary
langchain-huggingface
sentence-transformers
```

**Web**:
```
flask>=3.0.0
flask-cors
flask-sock
flasgger
```

**Data & Visualization**:
```
pandas
plotly
kaleido
```

**Development**:
```
pytest
black
flake8
python-dotenv
```

### 5.2 Environment Variables

```bash
# Database
DB_HOST=localhost
DB_NAME=chinook
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432

# LLM
ANTHROPIC_API_KEY=sk-ant-your-api-key

# Vector DB (for PGVector production)
VECTOR_DB_CONNECTION=postgresql://user:pass@localhost:5432/detomo_vectors

# App
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
LOG_LEVEL=INFO
```

### 5.3 Configuration

**File**: `config.py`
```python
import os
from pathlib import Path

class Config:
    # App
    APP_NAME = "Detomo SQL AI"
    VERSION = "1.0.0"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # Database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "chinook")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))

    # LLM
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    LLM_MODEL = "claude-3-5-sonnet-20241022"
    LLM_TEMPERATURE = 0.1
    LLM_MAX_TOKENS = 2048

    # Vector DB
    VECTOR_DB_PATH = "./detomo_vectordb"
    EMBEDDING_MODEL = "BAAI/bge-m3"
    N_RESULTS = 10

    # Training Data
    TRAINING_DATA_DIR = Path("training_data/chinook")

    # Flask
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = os.getenv("FLASK_DEBUG", "True") == "True"

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

class DevelopmentConfig(Config):
    DEBUG = True
    VECTOR_DB_CLIENT = "persistent"

class ProductionConfig(Config):
    DEBUG = False
    VECTOR_DB_CLIENT = "persistent"
    VECTOR_DB_CONNECTION = os.getenv("VECTOR_DB_CONNECTION")
```

---

## 6. IMPLEMENTATION PHASES

### Phase 1: Foundation (Week 1-2)
**Goal**: Setup cơ bản, training data, backend

**Tasks**:
- [ ] Setup project structure
- [ ] Install Chinook database
- [ ] Create training data files (DDL, docs, Q&A)
- [ ] Implement `DetomoVanna` class
- [ ] Write training script
- [ ] Train initial model
- [ ] Test SQL generation

**Deliverables**:
- Working Vanna backend
- Trained model with Chinook data
- 50+ Q&A pairs

### Phase 2: API Development (Week 3)
**Goal**: REST API endpoints

**Tasks**:
- [ ] Setup Flask app
- [ ] Implement core API endpoints
- [ ] Add error handling
- [ ] Add logging
- [ ] Write API tests
- [ ] API documentation (Swagger)

**Deliverables**:
- REST API with 6+ endpoints
- API documentation
- Test coverage ≥ 80%

### Phase 3: Frontend Development (Week 4-5)
**Goal**: Customize Vanna-Flask UI

**Tasks**:
- [ ] Clone vanna-flask repo
- [ ] Rebrand to Detomo SQL AI
- [ ] Implement chat interface
- [ ] Add visualization panel
- [ ] Implement admin panel
- [ ] Add Japanese language support
- [ ] Mobile responsive design

**Deliverables**:
- Fully functional web UI
- Admin dashboard
- Bilingual support

### Phase 4: Testing & Optimization (Week 6)
**Goal**: Quality assurance, performance tuning

**Tasks**:
- [ ] Write integration tests
- [ ] Performance testing
- [ ] SQL accuracy testing (50+ test queries)
- [ ] Load testing (100 concurrent users)
- [ ] Bug fixes
- [ ] Optimization (caching, indexing)

**Deliverables**:
- Test suite with ≥ 85% coverage
- Performance report
- Accuracy metrics ≥ 85%

### Phase 5: Deployment (Week 7)
**Goal**: Production deployment

**Tasks**:
- [ ] Docker containerization
- [ ] CI/CD pipeline setup
- [ ] Production database setup
- [ ] Environment configuration
- [ ] Monitoring & alerting
- [ ] Documentation

**Deliverables**:
- Deployed production app
- Monitoring dashboard
- User documentation

### Phase 6: Polish & Launch (Week 8)
**Goal**: Final touches, launch

**Tasks**:
- [ ] User acceptance testing
- [ ] Final bug fixes
- [ ] Training data expansion (100+ Q&A)
- [ ] Demo preparation
- [ ] Launch announcement

**Deliverables**:
- Production-ready app
- Demo video
- Launch materials

---

## 7. TASK BREAKDOWN

### 7.1 High Priority Tasks

#### Task 1: Setup Chinook Database
**Assignee**: Backend Developer
**Estimate**: 2 hours
**Steps**:
1. Download Chinook PostgreSQL scripts from https://github.com/lerocha/chinook-database
2. Create `chinook` database
3. Run DDL scripts (chinook_ddl.sql)
4. Load data (chinook_genres_artists_albums.sql, chinook_songs.sql)
5. Verify data loaded correctly
6. Create read-only user for app

#### Task 2: Create Training Data Files
**Assignee**: Data Engineer
**Estimate**: 16 hours
**Steps**:
1. Extract DDL for each table (11 files)
2. Write documentation for each table (11 files)
3. Write business rules documentation
4. Create basic Q&A pairs (20 questions)
5. Create aggregation Q&A pairs (15 questions)
6. Create join Q&A pairs (15 questions)
7. Create Japanese Q&A pairs (20 questions)
8. Review & validate all files

**Detailed Breakdown**:
- DDL extraction: 2 hours
- Documentation writing: 8 hours
- Q&A pair creation: 6 hours

#### Task 3: Implement DetomoVanna Class
**Assignee**: AI Engineer
**Estimate**: 8 hours
**Steps**:
1. Create `detomo_vanna.py`
2. Implement class inheriting ChromaDB + Anthropic
3. Add custom configuration
4. Add logging
5. Write unit tests
6. Test with sample queries

#### Task 4: Training Script Implementation
**Assignee**: AI Engineer
**Estimate**: 4 hours
**Steps**:
1. Create `scripts/train_chinook.py`
2. Implement DDL loading
3. Implement documentation loading
4. Implement Q&A loading
5. Add progress reporting
6. Add error handling
7. Test full training pipeline

#### Task 5: Flask API Development
**Assignee**: Backend Developer
**Estimate**: 16 hours
**Breakdown**:
- App setup: 2 hours
- Core endpoints: 8 hours
- Error handling: 2 hours
- Logging: 2 hours
- Testing: 2 hours

#### Task 6: UI Customization
**Assignee**: Frontend Developer
**Estimate**: 24 hours
**Breakdown**:
- Branding update: 4 hours
- Chat interface: 8 hours
- Admin panel: 8 hours
- Japanese translation: 4 hours

#### Task 7: Testing & QA
**Assignee**: QA Engineer
**Estimate**: 16 hours
**Breakdown**:
- Test case writing: 4 hours
- SQL accuracy testing: 6 hours
- Performance testing: 4 hours
- Bug reporting: 2 hours

### 7.2 Medium Priority Tasks

#### Task 8: Visualization Enhancement
**Estimate**: 8 hours
- Custom chart templates
- Color theme customization
- Export functionality

#### Task 9: Analytics Dashboard
**Estimate**: 12 hours
- Query metrics tracking
- Usage statistics
- Performance monitoring

#### Task 10: Documentation
**Estimate**: 8 hours
- User guide
- API documentation
- Deployment guide

### 7.3 Low Priority Tasks

#### Task 11: Advanced Features
**Estimate**: 16 hours
- Query history search
- Saved queries
- Query templates
- Multi-user support

#### Task 12: Performance Optimization
**Estimate**: 8 hours
- Caching layer
- Query optimization
- Database indexing

---

## 8. RISKS & MITIGATIONS

### Risk 1: Claude API Costs
**Impact**: High
**Probability**: Medium
**Mitigation**:
- Implement aggressive caching
- Rate limiting
- Use cheaper model for simple queries
- Monitor spending daily

### Risk 2: SQL Generation Accuracy < 85%
**Impact**: High
**Probability**: Medium
**Mitigation**:
- Extensive training data (100+ Q&A pairs)
- Iterative testing & refinement
- Fallback to simpler model
- Human-in-the-loop validation

### Risk 3: Performance Issues with Large Results
**Impact**: Medium
**Probability**: High
**Mitigation**:
- Limit result set size (1000 rows default)
- Pagination
- Async loading
- Query timeout (30s)

### Risk 4: Database Security
**Impact**: High
**Probability**: Low
**Mitigation**:
- Read-only database user
- SQL injection prevention
- Whitelist allowed tables
- Query validation

---

## 9. SUCCESS CRITERIA

### 9.1 MVP Requirements (Launch Criteria)
✅ Minimum Viable Product must have:

1. **Core Functionality**:
   - [ ] Natural language to SQL conversion works
   - [ ] SQL execution returns correct results
   - [ ] Basic visualization (bar, line charts)
   - [ ] Training data management

2. **Quality Metrics**:
   - [ ] SQL accuracy ≥ 75% (on 50 test queries)
   - [ ] Response time < 10s (p95)
   - [ ] No critical bugs

3. **User Experience**:
   - [ ] Clean, branded UI
   - [ ] Japanese & English support
   - [ ] Mobile-responsive
   - [ ] Error messages are helpful

4. **Data**:
   - [ ] Chinook database fully loaded
   - [ ] ≥ 50 Q&A training pairs
   - [ ] All 11 tables have DDL + docs

### 9.2 V1.0 Success Criteria

1. **Accuracy**: ≥ 85% SQL correctness
2. **Performance**: < 5s response time (p95)
3. **User Satisfaction**: ≥ 4/5 rating
4. **Coverage**: Support 100+ common query patterns
5. **Reliability**: 99% uptime

---

## 10. APPENDICES

### Appendix A: Sample Training Data

**DDL Example** (`training_data/chinook/ddl/invoice.sql`):
```sql
CREATE TABLE Invoice (
    InvoiceId INTEGER PRIMARY KEY,
    CustomerId INTEGER NOT NULL,
    InvoiceDate TIMESTAMP NOT NULL,
    BillingAddress VARCHAR(70),
    BillingCity VARCHAR(40),
    BillingState VARCHAR(40),
    BillingCountry VARCHAR(40),
    BillingPostalCode VARCHAR(10),
    Total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId)
);
```

**Documentation Example** (`training_data/chinook/documentation/invoice.md`):
```markdown
# Invoice Table

The Invoice table stores customer invoice information.

## Columns
- **InvoiceId**: Invoice ID (PK)
- **CustomerId**: Customer ID (FK → Customer)
- **InvoiceDate**: Invoice creation date
- **BillingCountry**: Billing country
- **Total**: Total invoice value

## Business Rules
- Each invoice belongs to 1 customer
- Total invoice = SUM(InvoiceLine.UnitPrice * Quantity)
- InvoiceDate is used to calculate revenue over time
```

**Q&A Example** (`training_data/chinook/questions/japanese_queries.json`):
```json
[
  {
    "question": "総売上はいくらですか？ / What is the total revenue?",
    "sql": "SELECT SUM(Total) as TotalRevenue FROM Invoice"
  },
  {
    "question": "最も多く支出した顧客は誰ですか？ / Which customer spent the most?",
    "sql": "SELECT c.FirstName, c.LastName, SUM(i.Total) as TotalSpent FROM Customer c JOIN Invoice i ON c.CustomerId = i.CustomerId GROUP BY c.CustomerId, c.FirstName, c.LastName ORDER BY TotalSpent DESC LIMIT 1"
  }
]
```

### Appendix B: API Response Examples

**Successful SQL Generation**:
```json
{
  "id": "req_abc123",
  "type": "sql_generation",
  "text": "SELECT c.FirstName, c.LastName, SUM(i.Total) as Revenue FROM Customer c JOIN Invoice i ON c.CustomerId = i.CustomerId GROUP BY c.CustomerId ORDER BY Revenue DESC LIMIT 10",
  "status": "success",
  "execution_time_ms": 1234,
  "metadata": {
    "model": "claude-3-5-sonnet-20241022",
    "tokens_used": 450,
    "similar_questions_found": 3
  }
}
```

**Error Response**:
```json
{
  "id": "req_abc124",
  "type": "error",
  "error": {
    "code": "SQL_GENERATION_FAILED",
    "message": "Could not generate SQL for the given question",
    "details": "Insufficient context about table 'xyz'",
    "suggestion": "Try asking about available tables first"
  },
  "status": "error"
}
```

### Appendix C: Testing Checklist

**SQL Accuracy Tests** (50 queries):
- [ ] Simple SELECT (5 queries)
- [ ] WHERE clauses (10 queries)
- [ ] JOINs (10 queries)
- [ ] GROUP BY / Aggregations (10 queries)
- [ ] ORDER BY / LIMIT (5 queries)
- [ ] Complex multi-table queries (10 queries)

**Performance Tests**:
- [ ] Response time < 5s for 95% of queries
- [ ] Handle 100 concurrent users
- [ ] Database connection pooling works
- [ ] Caching reduces repeat query time

**UI/UX Tests**:
- [ ] Chat interface responsive
- [ ] Visualizations render correctly
- [ ] Japanese characters display properly
- [ ] Mobile view works on 3 devices

---

## 11. CONTACT & RESOURCES

**Project Team**:
- Product Owner: [Name]
- Tech Lead: [Name]
- AI Engineer: [Name]
- Backend Developer: [Name]
- Frontend Developer: [Name]

**Resources**:
- Vanna Docs: https://vanna.ai/docs
- Chinook Database: https://github.com/lerocha/chinook-database
- Claude API Docs: https://docs.anthropic.com/claude/reference
- Vanna-Flask: https://github.com/vanna-ai/vanna-flask

**Repository**:
- GitHub: https://github.com/detomo/detomo-sql-ai

---

**Document Version History**:
- v1.0 (2025-10-25): Initial PRD
- [Future versions...]

---

**Approval**:
- [ ] Product Owner
- [ ] Tech Lead
- [ ] Stakeholders

---

**END OF PRD**
