# PRD: Detomo SQL AI

**Product Requirements Document**
**Version:** 2.0 (Vanna + Claude Agent SDK)
**Date:** 2025-10-26
**Author:** Detomo Team
**Status:** Draft

---

## 1. EXECUTIVE SUMMARY

### 1.1 Product Overview
Detomo SQL AI is an AI-powered Text-to-SQL application that allows users to query databases using natural language (Japanese/English), automatically generates SQL queries, and displays results visually.

**Architecture**: Uses **Vanna AI framework** as the core RAG pipeline with **Claude Agent SDK serving as the LLM endpoint** (instead of direct OpenAI/Anthropic API).

### 1.2 Technology Stack
- **RAG Framework**: Vanna AI (handles training, retrieval, SQL generation flow)
- **LLM Backend**: Claude Agent SDK as HTTP endpoint (replaces direct API calls)
- **LLM Model**: Claude Sonnet 4.5 (claude-sonnet-4-5)
- **Vector Database**: ChromaDB (managed by Vanna)
- **Embedding Model**: BAAI/bge-m3 (HuggingFace)
- **Target Database**: SQLite (Chinook database at data/chinook.db)
- **API Layer**: Flask (using Vanna's built-in Flask integration)
- **Frontend**: Vanna-Flask or Streamlit
- **Language**: Python 3.10+

### 1.3 Core Features
- Natural language to SQL conversion (powered by Vanna + Claude Agent SDK)
- Auto-generated visualizations (Vanna's Plotly integration)
- Training data management (Vanna's training methods)
- Interactive chat interface (Vanna-Flask)
- Japanese & English language support
- RAG-based context retrieval (Vanna + ChromaDB)

### 1.4 Why This Architecture?

**Vanna AI** handles:
- ✅ RAG pipeline (retrieve similar SQL, DDL, docs)
- ✅ Training data management
- ✅ Database connections
- ✅ SQL execution
- ✅ Visualization generation
- ✅ Web UI (Flask/Streamlit)

**Claude Agent SDK** only handles:
- ✅ LLM inference (receives prompts from Vanna, returns SQL)
- ✅ Serves as HTTP endpoint (Vanna calls this instead of OpenAI API)
- ✅ No database access, no tools, just text generation

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
5. **Modularity**: Clean separation (Vanna handles logic, Agent SDK handles LLM)

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

### 3.2 User Flows

#### Flow 1: Simple Query
```
User Input: "顧客は何人いますか？" / "How many customers are there?"
    ↓
Vanna retrieves similar queries from ChromaDB
    ↓
Vanna constructs prompt with context (DDL, docs, examples)
    ↓
Vanna sends prompt to Claude Agent SDK endpoint
    ↓
Claude Agent SDK returns: SELECT COUNT(*) FROM Customer
    ↓
Vanna executes SQL on chinook.db
    ↓
Display: "59人の顧客がいます" / "There are 59 customers"
```

#### Flow 2: Complex Query with Visualization
```
User Input: "2024年のジャンル別売上" / "Revenue by genre in 2024"
    ↓
Vanna retrieves relevant DDL (Genre, Track, InvoiceLine tables)
    ↓
Vanna retrieves similar join queries from training data
    ↓
Vanna constructs prompt → Claude Agent SDK
    ↓
Claude Agent SDK returns SQL with JOINs
    ↓
Vanna executes SQL → returns DataFrame
    ↓
Vanna auto-generates Plotly bar chart
    ↓
Display results + visualization
```

#### Flow 3: Training Data Management
```
Admin uses Vanna's training methods:
vn.train(ddl="CREATE TABLE Customer...")
vn.train(documentation="Customer table stores...")
vn.train(question="How many customers?", sql="SELECT COUNT(*) FROM Customer")
    ↓
Vanna stores in ChromaDB with embeddings (BAAI/bge-m3)
    ↓
Ready for inference
```

---

## 4. ARCHITECTURE & TECHNICAL DESIGN

### 4.1 System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                           │
│                  (Vanna-Flask / Streamlit)                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ User question
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Vanna AI Framework                          │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 1. RAG Retrieval (ChromaDB)                              │   │
│  │    - Similar SQL queries                                 │   │
│  │    - Relevant DDL                                        │   │
│  │    - Documentation                                       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                             ↓                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 2. Prompt Construction                                   │   │
│  │    - Build context from retrieved data                   │   │
│  │    - Format prompt for LLM                               │   │
│  └──────────────────────────────────────────────────────────┘   │
│                             ↓                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 3. submit_prompt() → Custom LLM Class                    │   │
│  └──────────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP POST /generate
                            │ {"prompt": "...", "model": "claude-sonnet-4-5"}
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│              Claude Agent SDK (HTTP Endpoint Server)             │
│                                                                   │
│  - Receives prompt from Vanna                                    │
│  - Calls Claude API (claude-sonnet-4-5)                          │
│  - Returns generated SQL text                                    │
│  - No database access, no tools, just LLM inference             │
└───────────────────────────┬─────────────────────────────────────┘
                            │ Return SQL text
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Vanna AI Framework                          │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 4. SQL Execution                                         │   │
│  │    - Validate SQL                                        │   │
│  │    - Execute on chinook.db                               │   │
│  │    - Return DataFrame                                    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                             ↓                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 5. Visualization (Optional)                              │   │
│  │    - Auto-detect chart type                              │   │
│  │    - Generate Plotly figure                              │   │
│  └──────────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ↓
                    Return to User Interface
```

### 4.2 Component Details

#### 4.2.1 Vanna AI Framework (Core)

Vanna handles the entire RAG pipeline:

**Training Phase**:
```python
vn.train(ddl="CREATE TABLE Customer ...")
vn.train(documentation="Customer table documentation...")
vn.train(question="How many customers?", sql="SELECT COUNT(*) FROM Customer")
```

**Query Phase**:
```python
sql = vn.generate_sql("How many customers are there?")
# Vanna internally:
# 1. Retrieves similar queries from ChromaDB
# 2. Constructs prompt with context
# 3. Calls submit_prompt() → Claude Agent SDK
# 4. Returns generated SQL

df = vn.run_sql(sql)  # Execute SQL
fig = vn.get_plotly_figure(sql, df)  # Generate chart
```

#### 4.2.2 Custom Vanna Class with Claude Agent SDK

**File**: `src/detomo_vanna.py`

```python
from vanna.base import VannaBase
from vanna.chromadb import ChromaDB_VectorStore
import requests
import os

class ClaudeAgentChat(VannaBase):
    """
    Custom Vanna LLM class that calls Claude Agent SDK endpoint.

    This class implements Vanna's LLM interface to use Claude Agent SDK
    as the LLM backend instead of OpenAI/Anthropic API directly.
    """

    def __init__(self, config=None):
        VannaBase.__init__(self, config=config)

        # Claude Agent SDK endpoint
        self.agent_endpoint = config.get("agent_endpoint", "http://localhost:8000/generate")
        self.model = config.get("model", "claude-sonnet-4-5")
        self.temperature = config.get("temperature", 0.1)
        self.max_tokens = config.get("max_tokens", 2048)

    def system_message(self, message: str) -> dict:
        """Format system message (Vanna interface)"""
        return {"role": "system", "content": message}

    def user_message(self, message: str) -> dict:
        """Format user message (Vanna interface)"""
        return {"role": "user", "content": message}

    def assistant_message(self, message: str) -> dict:
        """Format assistant message (Vanna interface)"""
        return {"role": "assistant", "content": message}

    def submit_prompt(self, prompt, **kwargs) -> str:
        """
        Send prompt to Claude Agent SDK endpoint.

        This is the main method Vanna calls to get LLM responses.

        Args:
            prompt: List of message dicts or string

        Returns:
            str: Generated SQL or text from Claude
        """

        # Convert prompt to string if it's a list of messages
        if isinstance(prompt, list):
            # Extract just the content from messages
            prompt_text = "\n\n".join([
                f"{msg.get('role', 'user')}: {msg.get('content', '')}"
                for msg in prompt
            ])
        else:
            prompt_text = str(prompt)

        # Call Claude Agent SDK endpoint
        try:
            response = requests.post(
                self.agent_endpoint,
                json={
                    "prompt": prompt_text,
                    "model": self.model,
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens
                },
                timeout=30
            )
            response.raise_for_status()

            result = response.json()
            return result.get("text", "")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling Claude Agent SDK: {str(e)}")


class DetomoVanna(ChromaDB_VectorStore, ClaudeAgentChat):
    """
    Main Vanna class for Detomo SQL AI.

    Combines:
    - ChromaDB_VectorStore: For RAG retrieval
    - ClaudeAgentChat: For LLM generation via Claude Agent SDK
    """

    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        ClaudeAgentChat.__init__(self, config=config)
```

**Usage**:

```python
from src.detomo_vanna import DetomoVanna

# Initialize Vanna with Claude Agent SDK as LLM
vn = DetomoVanna(config={
    # ChromaDB settings (managed by Vanna)
    "path": "./detomo_vectordb",
    "client": "persistent",
    "embedding_function": "sentence-transformers/BAAI-bge-m3",

    # Claude Agent SDK settings
    "agent_endpoint": "http://localhost:8000/generate",
    "model": "claude-sonnet-4-5",
    "temperature": 0.1,
    "max_tokens": 2048
})

# Connect to database (Vanna handles this)
vn.connect_to_sqlite("data/chinook.db")

# Train (Vanna handles storage in ChromaDB)
vn.train(ddl="CREATE TABLE Customer ...")
vn.train(question="How many customers?", sql="SELECT COUNT(*) FROM Customer")

# Query (Vanna orchestrates RAG + Claude Agent SDK)
sql = vn.generate_sql("顧客は何人いますか？")
df = vn.run_sql(sql)
print(df)
```

#### 4.2.3 Claude Agent SDK Server

**File**: `claude_agent_server.py`

```python
from flask import Flask, request, jsonify
import asyncio
import os
from dotenv import load_dotenv
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock

load_dotenv()

app = Flask(__name__)


@app.route("/generate", methods=["POST"])
def generate():
    """
    LLM endpoint for Vanna using Claude Agent SDK.

    Receives prompt from Vanna, uses Claude Agent SDK, returns text.
    No database access, no tools, just simple LLM inference.

    Request:
        {
            "prompt": "...",
            "model": "claude-sonnet-4-5",
            "temperature": 0.1,
            "max_tokens": 2048
        }

    Response:
        {
            "text": "SELECT COUNT(*) FROM Customer",
            "model": "claude-sonnet-4-5"
        }
    """

    data = request.json
    prompt = data.get("prompt", "")
    model = data.get("model", "claude-sonnet-4-5")
    temperature = data.get("temperature", 0.1)
    max_tokens = data.get("max_tokens", 2048)

    if not prompt:
        return jsonify({"error": "Missing prompt"}), 400

    try:
        # Run async Claude Agent SDK call
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            call_claude_agent(prompt, model, temperature, max_tokens)
        )
        loop.close()

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


async def call_claude_agent(prompt: str, model: str, temperature: float, max_tokens: int):
    """
    Call Claude Agent SDK to generate SQL.

    Uses minimal configuration - no tools, no complex system prompt.
    Just basic LLM inference for Vanna.
    """

    # Simple system prompt for SQL generation
    system_prompt = """You are a SQL expert. Generate accurate SQL queries based on the given context.

Rules:
- Generate ONLY the SQL query, no explanation
- Use proper SQL syntax
- Follow the database schema provided in the prompt
- Use similar examples as reference when provided"""

    # Configure Agent SDK with minimal options
    # Note: API key is set via ANTHROPIC_API_KEY environment variable
    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
        model=model,
        permission_mode="bypassPermissions",  # No file access needed
        max_turns=1,  # Single turn - just generate SQL
        allowed_tools=[]  # No tools needed for simple LLM inference
    )

    # Use Agent SDK (API key from environment variable)
    async with ClaudeSDKClient(options=options) as client:

        # Send query to agent
        await client.query(prompt)

        # Collect response
        response_text = ""
        async for message in client.receive_response():
            # Check if it's an AssistantMessage
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    # Extract text from TextBlock
                    if isinstance(block, TextBlock):
                        response_text += block.text

        return {
            "text": response_text.strip(),
            "model": model
        }


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Claude Agent SDK LLM Endpoint",
        "version": "1.0.0"
    })


if __name__ == "__main__":
    # Make sure ANTHROPIC_API_KEY is set in environment
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("WARNING: ANTHROPIC_API_KEY not found in environment variables!")

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )
```

**Run the server**:
```bash
python claude_agent_server.py
# Server runs on http://localhost:8000
```

**Test the endpoint**:
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Generate SQL to count customers in Customer table",
    "model": "claude-sonnet-4-5",
    "temperature": 0.1
  }'

# Response:
# {
#   "text": "SELECT COUNT(*) FROM Customer",
#   "model": "claude-sonnet-4-5"
# }
```

### 4.3 Data Flow

**Complete flow khi user hỏi "How many customers?"**:

1. **User → Vanna-Flask UI**
   ```
   User inputs: "How many customers are there?"
   ```

2. **Vanna retrieves context from ChromaDB**
   ```python
   # Vanna internally does semantic search
   similar_questions = chromadb.query("How many customers?", n_results=5)
   # Returns:
   # - Similar Q&A pairs
   # - Customer table DDL
   # - Customer table documentation
   ```

3. **Vanna constructs prompt**
   ```python
   prompt = f"""
   You are a SQL expert. Generate SQL for the following question.

   Database Schema (DDL):
   CREATE TABLE Customer (
       CustomerId INTEGER PRIMARY KEY,
       FirstName VARCHAR(40),
       LastName VARCHAR(20),
       Email VARCHAR(60)
   );

   Similar Questions:
   Q: "How many users?" → SELECT COUNT(*) FROM Customer
   Q: "Total customers" → SELECT COUNT(*) FROM Customer

   Question: How many customers are there?

   Generate only the SQL query, no explanation.
   """
   ```

4. **Vanna calls Claude Agent SDK**
   ```python
   response = requests.post("http://localhost:8000/generate", json={
       "prompt": prompt,
       "model": "claude-sonnet-4-5",
       "temperature": 0.1
   })
   sql = response.json()["text"]  # "SELECT COUNT(*) FROM Customer"
   ```

5. **Claude Agent SDK calls Anthropic API**
   ```python
   # Inside claude_agent_server.py
   message = anthropic_client.messages.create(
       model="claude-sonnet-4-5-20250929",
       messages=[{"role": "user", "content": prompt}]
   )
   text = message.content[0].text
   return {"text": text}
   ```

6. **Vanna executes SQL**
   ```python
   df = vn.run_sql("SELECT COUNT(*) FROM Customer")
   # Returns: DataFrame with count
   ```

7. **Vanna returns to UI**
   ```python
   {
       "sql": "SELECT COUNT(*) FROM Customer",
       "df": [[59]],
       "columns": ["COUNT(*)"]
   }
   ```

### 4.4 Training Data Management

Vanna provides built-in methods for training data management:

**File**: `scripts/train_chinook.py`

```python
from src.detomo_vanna import DetomoVanna
import os
import json
from pathlib import Path

def train_chinook_database():
    """
    Load training data into Vanna (stored in ChromaDB).
    """

    # Initialize Vanna
    vn = DetomoVanna(config={
        "path": "./detomo_vectordb",
        "client": "persistent",
        "agent_endpoint": "http://localhost:8000/generate",
        "model": "claude-sonnet-4-5"
    })

    # Connect to database
    vn.connect_to_sqlite("data/chinook.db")

    # 1. Train DDL (Vanna will store in ChromaDB)
    print("Training DDL...")
    ddl_dir = Path("training_data/chinook/ddl")
    for ddl_file in ddl_dir.glob("*.sql"):
        with open(ddl_file, 'r', encoding='utf-8') as f:
            ddl_content = f.read()
            vn.train(ddl=ddl_content)
            print(f"✓ Trained {ddl_file.name}")

    # 2. Train Documentation (Vanna will store in ChromaDB)
    print("\nTraining Documentation...")
    doc_dir = Path("training_data/chinook/documentation")
    for doc_file in doc_dir.glob("*.md"):
        with open(doc_file, 'r', encoding='utf-8') as f:
            doc_content = f.read()
            vn.train(documentation=doc_content)
            print(f"✓ Trained {doc_file.name}")

    # 3. Train Q&A Pairs (Vanna will store in ChromaDB)
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
    training_data = vn.get_training_data()
    print(f"\nTotal training items: {len(training_data)}")

if __name__ == "__main__":
    train_chinook_database()
```

### 4.5 Flask API (Using Vanna)

**File**: `app.py`

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.detomo_vanna import DetomoVanna
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Vanna once
vn = DetomoVanna(config={
    "path": "./detomo_vectordb",
    "client": "persistent",
    "agent_endpoint": os.getenv("CLAUDE_AGENT_ENDPOINT", "http://localhost:8000/generate"),
    "model": "claude-sonnet-4-5"
})

# Connect to database
vn.connect_to_sqlite("data/chinook.db")


@app.route("/api/v0/query", methods=["POST"])
def query():
    """
    Main endpoint for natural language SQL queries.

    Vanna handles everything:
    - RAG retrieval
    - Prompt construction
    - LLM call (via Claude Agent SDK)
    - SQL execution
    - Visualization
    """

    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"error": "Missing 'question' field"}), 400

    try:
        # Generate SQL (Vanna + Claude Agent SDK)
        sql = vn.generate_sql(question)

        # Execute SQL (Vanna)
        df = vn.run_sql(sql)

        # Generate visualization if applicable (Vanna)
        fig = None
        try:
            fig = vn.get_plotly_figure(sql=sql, df=df, question=question)
            fig_json = fig.to_json() if fig else None
        except:
            fig_json = None

        return jsonify({
            "sql": sql,
            "results": df.to_dict(orient='records'),
            "columns": df.columns.tolist(),
            "visualization": fig_json
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/v0/train", methods=["POST"])
def train():
    """Add training data to Vanna"""

    data = request.json
    training_type = data.get("type")  # "ddl", "documentation", "sql"

    try:
        if training_type == "ddl":
            vn.train(ddl=data.get("content"))
        elif training_type == "documentation":
            vn.train(documentation=data.get("content"))
        elif training_type == "sql":
            vn.train(
                question=data.get("question"),
                sql=data.get("sql")
            )
        else:
            return jsonify({"error": "Invalid type"}), 400

        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/v0/training_data", methods=["GET"])
def get_training_data():
    """Get all training data from Vanna"""

    try:
        training_data = vn.get_training_data()
        return jsonify({
            "data": training_data.to_dict(orient='records'),
            "count": len(training_data)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/v0/health", methods=["GET"])
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "framework": "Vanna AI",
        "llm": "Claude Agent SDK"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
```

---

## 5. FRONTEND / UI LAYER

### 5.1 UI Architecture Overview

**Based on**: [vanna-flask](https://github.com/vanna-ai/vanna-flask) architecture

**Technology Stack**:
- **Backend**: Flask serving static files + REST API
- **Frontend**: Single-Page Application (SPA)
- **Framework**: React/Vue (bundled as static assets)
- **Styling**: Tailwind CSS with dark mode support
- **Charts**: Plotly.js for interactive visualizations
- **Typography**: Roboto Slab (Google Fonts)

**Branding**: "Detomo SQL Agent" (replacing "Vanna.AI")

### 5.2 UI Components

#### 5.2.1 Main Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Detomo SQL Agent                                    [Logo]  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Chat Interface                                      │    │
│  │  ┌──────────────────────────────────────────────┐   │    │
│  │  │ Suggested Questions:                         │   │    │
│  │  │ • How many customers do we have?             │   │    │
│  │  │ • Show top 10 albums by sales                │   │    │
│  │  │ • Revenue by genre in 2024                   │   │    │
│  │  └──────────────────────────────────────────────┘   │    │
│  │                                                       │    │
│  │  ┌──────────────────────────────────────────────┐   │    │
│  │  │ 💬 User: How many customers?                 │   │    │
│  │  └──────────────────────────────────────────────┘   │    │
│  │                                                       │    │
│  │  ┌──────────────────────────────────────────────┐   │    │
│  │  │ 🤖 SQL Generated:                            │   │    │
│  │  │ SELECT COUNT(*) FROM Customer                │   │    │
│  │  │                                              │   │    │
│  │  │ Results:                                     │   │    │
│  │  │ ┌──────────┐                                 │   │    │
│  │  │ │ COUNT(*) │                                 │   │    │
│  │  │ ├──────────┤                                 │   │    │
│  │  │ │    59    │                                 │   │    │
│  │  │ └──────────┘                                 │   │    │
│  │  │                                              │   │    │
│  │  │ [Download CSV]  [Copy SQL]                   │   │    │
│  │  └──────────────────────────────────────────────┘   │    │
│  │                                                       │    │
│  │  ┌──────────────────────────────────────────────┐   │    │
│  │  │ 📊 Visualization (if applicable)             │   │    │
│  │  │  [Interactive Plotly Chart]                  │   │    │
│  │  └──────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Ask a question... 💬                           [Send]│   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│ Sidebar: [Query History] [Training Data] [Settings]          │
└─────────────────────────────────────────────────────────────┘
```

#### 5.2.2 Component Breakdown

**1. Header**
- Detomo SQL Agent logo/title
- Dark mode toggle
- Settings menu

**2. Suggested Questions** (on load)
- Display 3-5 example questions via `/api/v0/generate_questions`
- Clickable to auto-fill input

**3. Chat Interface**
- Message history with user questions and AI responses
- Each response contains:
  - Generated SQL (with syntax highlighting)
  - Query results (as table)
  - Visualization (if applicable)
  - Action buttons: Download CSV, Copy SQL, Share

**4. Input Area**
- Text input for natural language questions
- Bilingual support (EN/JP)
- Submit button
- Loading indicator during query processing

**5. Sidebar**
- **Query History**: Previous questions (via `/api/v0/get_question_history`)
- **Training Data**: View/manage training examples (via `/api/v0/get_training_data`)
- **Settings**: Model config, language preference

### 5.3 API Endpoints (Frontend Integration)

Following vanna-flask pattern, the UI interacts with these endpoints:

**Core Query Flow**:
1. `GET /api/v0/generate_questions` - Get suggested questions on page load
2. `POST /api/v0/generate_sql` - Convert NL to SQL (cache result with ID)
3. `GET /api/v0/run_sql?id={query_id}` - Execute SQL from cached query
4. `GET /api/v0/generate_plotly_figure?id={query_id}` - Generate chart
5. `GET /api/v0/generate_followup_questions?id={query_id}` - Suggest related questions

**History & State**:
6. `GET /api/v0/get_question_history` - Load all previous queries
7. `GET /api/v0/load_question?id={query_id}` - Load complete cached state

**Training Data Management**:
8. `GET /api/v0/get_training_data` - View training examples
9. `POST /api/v0/train` - Add new training data
10. `POST /api/v0/remove_training_data` - Delete training example

**Utilities**:
11. `GET /api/v0/download_csv?id={query_id}` - Export results as CSV

### 5.4 Frontend Implementation (app.py updates)

**File**: `app.py` (update from Section 4.5)

Add the following endpoints to support vanna-flask UI pattern:

```python
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from src.detomo_vanna import DetomoVanna
from cache import MemoryCache
import os
from dotenv import load_dotenv
import uuid
import pandas as pd

load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Initialize Vanna once
vn = DetomoVanna(config={
    "path": "./detomo_vectordb",
    "client": "persistent",
    "agent_endpoint": os.getenv("CLAUDE_AGENT_ENDPOINT", "http://localhost:8000/generate"),
    "model": "claude-sonnet-4-5"
})

# Connect to database
vn.connect_to_sqlite("data/chinook.db")

# Initialize cache for query state management
cache = MemoryCache()

# Decorator for cache validation
def requires_cache(fields):
    def decorator(f):
        def wrapper(*args, **kwargs):
            query_id = request.args.get('id')
            if not query_id:
                return jsonify({"error": "Missing 'id' parameter"}), 400

            if not cache.get(id=query_id, field=fields[0]):
                return jsonify({"error": "Query ID not found in cache"}), 404

            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator


# Serve frontend
@app.route("/")
def index():
    """Serve the main SPA"""
    return app.send_static_file('index.html')


# 1. Generate suggested questions on page load
@app.route("/api/v0/generate_questions", methods=["GET"])
def generate_questions():
    """
    Generate suggested questions based on training data.
    Called when user first loads the UI.
    """
    try:
        questions = vn.generate_questions()
        return jsonify({
            "questions": questions,
            "type": "question_list"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 2. Generate SQL from natural language
@app.route("/api/v0/generate_sql", methods=["GET"])
def generate_sql():
    """
    Convert natural language to SQL via Vanna + Claude Agent SDK.
    Cache the result with unique ID.
    """
    question = request.args.get('question')

    if not question:
        return jsonify({"error": "Missing 'question' parameter"}), 400

    try:
        # Generate SQL via Vanna (calls Claude Agent SDK)
        sql = vn.generate_sql(question)

        # Create unique ID and cache the result
        query_id = cache.generate_id()
        cache.set(id=query_id, field='question', value=question)
        cache.set(id=query_id, field='sql', value=sql)

        return jsonify({
            "id": query_id,
            "text": sql,
            "type": "sql"
        })

    except Exception as e:
        return jsonify({
            "type": "error",
            "error": str(e)
        }), 500


# 3. Execute SQL and cache results
@app.route("/api/v0/run_sql", methods=["GET"])
@requires_cache(['sql'])
def run_sql():
    """
    Execute SQL query and store DataFrame in cache.
    Requires 'id' parameter from generate_sql.
    """
    query_id = request.args.get('id')

    try:
        sql = cache.get(id=query_id, field='sql')

        # Execute SQL via Vanna
        df = vn.run_sql(sql)

        # Cache the DataFrame
        cache.set(id=query_id, field='df', value=df)

        return jsonify({
            "type": "df",
            "id": query_id,
            "df": df.to_json(orient='records'),
            "columns": df.columns.tolist()
        })

    except Exception as e:
        return jsonify({
            "type": "error",
            "error": str(e)
        }), 500


# 4. Generate visualization
@app.route("/api/v0/generate_plotly_figure", methods=["GET"])
@requires_cache(['sql', 'df'])
def generate_plotly_figure():
    """
    Generate Plotly chart from cached SQL and DataFrame.
    """
    query_id = request.args.get('id')

    try:
        sql = cache.get(id=query_id, field='sql')
        df = cache.get(id=query_id, field='df')
        question = cache.get(id=query_id, field='question')

        # Generate chart via Vanna
        fig = vn.get_plotly_figure(sql=sql, df=df, question=question)

        # Cache the figure
        if fig:
            cache.set(id=query_id, field='fig', value=fig.to_json())

            return jsonify({
                "type": "plotly",
                "id": query_id,
                "fig": fig.to_json()
            })
        else:
            return jsonify({
                "type": "error",
                "error": "Could not generate visualization"
            }), 400

    except Exception as e:
        return jsonify({
            "type": "error",
            "error": str(e)
        }), 500


# 5. Generate followup questions
@app.route("/api/v0/generate_followup_questions", methods=["GET"])
@requires_cache(['sql', 'df'])
def generate_followup_questions():
    """
    Generate related questions based on current query.
    """
    query_id = request.args.get('id')

    try:
        question = cache.get(id=query_id, field='question')
        sql = cache.get(id=query_id, field='sql')
        df = cache.get(id=query_id, field='df')

        # Generate followup questions via Vanna
        followup = vn.generate_followup_questions(question=question, sql=sql, df=df)

        # Cache followup questions
        cache.set(id=query_id, field='followup_questions', value=followup)

        return jsonify({
            "type": "question_list",
            "id": query_id,
            "questions": followup
        })

    except Exception as e:
        return jsonify({
            "type": "error",
            "error": str(e)
        }), 500


# 6. Load complete cached query state
@app.route("/api/v0/load_question", methods=["GET"])
@requires_cache(['question'])
def load_question():
    """
    Load all cached data for a specific query ID.
    Used when clicking on query history.
    """
    query_id = request.args.get('id')

    try:
        question = cache.get(id=query_id, field='question')
        sql = cache.get(id=query_id, field='sql')
        df = cache.get(id=query_id, field='df')
        fig = cache.get(id=query_id, field='fig')
        followup = cache.get(id=query_id, field='followup_questions')

        result = {
            "type": "question_cache",
            "id": query_id,
            "question": question,
            "sql": sql
        }

        if df is not None:
            result["df"] = df.to_json(orient='records')
            result["columns"] = df.columns.tolist()

        if fig is not None:
            result["fig"] = fig

        if followup is not None:
            result["followup_questions"] = followup

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "type": "error",
            "error": str(e)
        }), 500


# 7. Get query history
@app.route("/api/v0/get_question_history", methods=["GET"])
def get_question_history():
    """
    Return all cached questions.
    Used for sidebar query history.
    """
    try:
        history = cache.get_all(field='question')

        return jsonify({
            "type": "question_history",
            "questions": history
        })

    except Exception as e:
        return jsonify({
            "type": "error",
            "error": str(e)
        }), 500


# 8. Get training data
@app.route("/api/v0/get_training_data", methods=["GET"])
def get_training_data():
    """
    Get all training data from Vanna.
    Used for training data management UI.
    """
    try:
        training_data = vn.get_training_data()

        return jsonify({
            "type": "df",
            "df": training_data.to_json(orient='records')
        })

    except Exception as e:
        return jsonify({
            "type": "error",
            "error": str(e)
        }), 500


# 9. Add training data
@app.route("/api/v0/train", methods=["POST"])
def train():
    """
    Add new training data to Vanna.

    Request body options:
    1. {"type": "ddl", "ddl": "CREATE TABLE ..."}
    2. {"type": "documentation", "documentation": "..."}
    3. {"type": "sql", "question": "...", "sql": "..."}
    """
    data = request.json

    try:
        if data.get("ddl"):
            vn.train(ddl=data["ddl"])
            return jsonify({"status": "success", "message": "DDL added"})

        elif data.get("documentation"):
            vn.train(documentation=data["documentation"])
            return jsonify({"status": "success", "message": "Documentation added"})

        elif data.get("question") and data.get("sql"):
            vn.train(question=data["question"], sql=data["sql"])
            return jsonify({"status": "success", "message": "Q&A pair added"})

        else:
            return jsonify({"error": "Invalid training data format"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 10. Remove training data
@app.route("/api/v0/remove_training_data", methods=["POST"])
def remove_training_data():
    """
    Remove training data from Vanna by ID.

    Request: {"id": "training_data_id"}
    """
    data = request.json
    training_id = data.get("id")

    if not training_id:
        return jsonify({"error": "Missing 'id' field"}), 400

    try:
        vn.remove_training_data(id=training_id)
        return jsonify({"status": "success", "message": "Training data removed"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 11. Download CSV
@app.route("/api/v0/download_csv", methods=["GET"])
@requires_cache(['df'])
def download_csv():
    """
    Export query results as CSV file.
    """
    query_id = request.args.get('id')

    try:
        df = cache.get(id=query_id, field='df')
        question = cache.get(id=query_id, field='question')

        # Save to temporary file
        csv_filename = f"detomo_sql_results_{query_id}.csv"
        csv_path = f"/tmp/{csv_filename}"
        df.to_csv(csv_path, index=False)

        return send_file(
            csv_path,
            mimetype='text/csv',
            as_attachment=True,
            download_name=csv_filename
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Health check
@app.route("/api/v0/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "framework": "Vanna AI",
        "llm": "Claude Agent SDK",
        "version": "1.0.0"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
```

### 5.5 Cache Implementation

**File**: `cache.py`

```python
import uuid

class MemoryCache:
    """
    In-memory cache for storing query state across API calls.

    Based on vanna-flask cache pattern.
    Each query ID stores: question, sql, df, fig, followup_questions
    """

    def __init__(self):
        self.cache = {}

    def generate_id(self) -> str:
        """Generate unique ID for cache entry"""
        return str(uuid.uuid4())

    def set(self, id: str, field: str, value):
        """Set a field for a specific ID"""
        if id not in self.cache:
            self.cache[id] = {}

        self.cache[id][field] = value

    def get(self, id: str, field: str):
        """Get a field for a specific ID"""
        if id not in self.cache:
            return None

        return self.cache[id].get(field)

    def get_all(self, field: str) -> list:
        """
        Get all values of a specific field across all cached entries.
        Used for query history (field='question').

        Returns list of dicts: [{"id": "...", "value": "..."}]
        """
        result = []
        for cache_id, cache_data in self.cache.items():
            if field in cache_data:
                result.append({
                    "id": cache_id,
                    field: cache_data[field]
                })

        return result

    def delete(self, id: str):
        """Delete entire cache entry by ID"""
        if id in self.cache:
            del self.cache[id]
```

### 5.6 Frontend Static Files Structure

```
static/
├── index.html                  # Main SPA entry point
├── detomo_logo.svg            # Detomo branding (replace vanna.svg)
└── assets/
    ├── index-[hash].js        # Bundled React/Vue app
    └── index-[hash].css       # Tailwind CSS + custom styles
```

**File**: `static/index.html` (template)

```html
<!DOCTYPE html>
<html lang="en" class="bg-white dark:bg-slate-900">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Detomo SQL Agent</title>

    <!-- Plotly.js for charts -->
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;600;700&display=swap" rel="stylesheet">

    <!-- App CSS -->
    <link rel="stylesheet" href="/assets/index.css" />
</head>
<body>
    <div id="app"></div>

    <!-- App JS -->
    <script type="module" src="/assets/index.js"></script>
</body>
</html>
```

### 5.7 Key UI/UX Features

**1. Dark Mode Support**
- Tailwind CSS dark mode classes (`dark:bg-slate-900`)
- Toggle in header
- Persist preference in localStorage

**2. Bilingual Support (EN/JP)**
- Language toggle in settings
- All UI strings translated
- Natural language input accepts both languages

**3. Query Flow UX**
- Suggested questions on page load
- Real-time loading indicators
- Smooth transitions between: question → SQL → results → chart
- Followup questions after each result

**4. Interactive Results**
- Copy SQL button (copy to clipboard)
- Download CSV button
- Interactive Plotly charts (zoom, pan, hover)
- Share query via URL (using query ID)

**5. History & State Management**
- Sidebar shows previous queries
- Click any history item to reload full state
- Cache persists during session (memory-based)

### 5.8 Customization for Detomo Branding

**Changes from vanna-flask**:

| Original | Detomo Version |
|----------|----------------|
| Title: "Vanna.AI" | Title: "Detomo SQL Agent" |
| Logo: vanna.svg | Logo: detomo_logo.svg |
| Color scheme: Default | Color scheme: Detomo brand colors |
| Footer: "Powered by Vanna" | Footer: "Powered by Detomo AI" |
| Example questions: Generic | Example questions: Chinook-specific |

---

## 6. TECHNICAL SPECIFICATIONS

### 6.1 Dependencies

**File**: `requirements.txt`

```
# Vanna AI
vanna==0.7.9

# Claude Agent SDK
claude-agent-sdk>=0.1.0
anthropic>=0.40.0

# API
flask>=3.0.0
flask-cors>=4.0.0
requests>=2.31.0

# Vector Database (used by Vanna)
chromadb<1.0.0
sentence-transformers>=2.2.0

# Utilities
python-dotenv>=1.0.0
pandas>=2.0.0
plotly>=5.14.0

# Development
pytest>=7.4.0
```

### 6.2 Environment Variables

**File**: `.env`

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

### 6.3 Project Structure

```
detomo-sql-ai/
├── .env                          # Environment variables
├── requirements.txt              # Python dependencies
├── PRD.md                        # This file
│
├── claude_agent_server.py        # Claude Agent SDK HTTP endpoint
├── app.py                        # Flask API + UI server (vanna-flask pattern)
├── cache.py                      # Memory cache for query state
│
├── data/
│   └── chinook.db               # SQLite database
│
├── static/                       # Frontend UI files
│   ├── index.html               # Main SPA entry point
│   ├── detomo_logo.svg          # Detomo branding
│   └── assets/                  # Bundled frontend assets
│       ├── index-[hash].js      # React/Vue app bundle
│       └── index-[hash].css     # Tailwind CSS + custom styles
│
├── src/
│   ├── __init__.py
│   └── detomo_vanna.py          # Custom Vanna class
│
├── scripts/
│   └── train_chinook.py         # Training script
│
├── training_data/
│   └── chinook/                 # Training data files
│       ├── ddl/                 # DDL files
│       ├── documentation/       # Markdown docs
│       └── questions/           # Q&A JSON files
│
├── detomo_vectordb/             # ChromaDB storage (auto-created by Vanna)
│
└── tests/
    ├── test_vanna.py            # Vanna integration tests
    ├── test_agent_endpoint.py   # Claude Agent SDK tests
    └── test_api_endpoints.py    # UI API endpoints tests
```

---

## 7. IMPLEMENTATION PHASES

### Phase 1: Setup Claude Agent SDK Endpoint (Week 1)
**Goal**: Create simple HTTP endpoint for LLM

**Tasks**:
- [ ] Create `claude_agent_server.py`
- [ ] Implement `/generate` endpoint
- [ ] Test with sample prompts
- [ ] Add error handling

**Deliverables**:
- Working HTTP endpoint on http://localhost:8000
- Can receive prompt and return SQL

### Phase 2: Vanna Integration (Week 2)
**Goal**: Integrate Vanna with Claude Agent SDK

**Tasks**:
- [ ] Create custom Vanna class (`DetomoVanna`)
- [ ] Implement `submit_prompt()` to call Claude Agent SDK
- [ ] Test RAG retrieval
- [ ] Test SQL generation

**Deliverables**:
- Working Vanna + Claude Agent SDK integration
- Can generate SQL from natural language

### Phase 3: Training Data (Week 3)
**Goal**: Load Chinook training data

**Tasks**:
- [ ] Create training script
- [ ] Load DDL files
- [ ] Load documentation
- [ ] Load Q&A pairs
- [ ] Verify ChromaDB storage

**Deliverables**:
- Fully trained Vanna model
- 50+ training examples loaded

### Phase 4: Flask API (Week 4)
**Goal**: Build REST API

**Tasks**:
- [ ] Create Flask app using Vanna
- [ ] Implement `/api/v0/query` endpoint
- [ ] Implement `/api/v0/train` endpoint
- [ ] Add error handling
- [ ] API documentation

**Deliverables**:
- REST API with 3+ endpoints
- Postman collection

### Phase 5: Testing & Optimization (Week 5)
**Goal**: QA and performance tuning

**Tasks**:
- [ ] SQL accuracy testing (50+ queries)
- [ ] Performance benchmarking
- [ ] Bug fixes
- [ ] Prompt optimization

**Deliverables**:
- Test suite with ≥80% coverage
- Accuracy ≥85%

### Phase 6: Frontend (Week 6-7)
**Goal**: Build Detomo SQL Agent UI (based on vanna-flask)

**Tasks**:
- [ ] Update `app.py` with vanna-flask API endpoints
- [ ] Implement `cache.py` for query state management
- [ ] Create `static/index.html` with Detomo branding
- [ ] Build React/Vue SPA frontend (or fork vanna-flask)
- [ ] Implement chat interface with SQL results display
- [ ] Add Plotly visualization rendering
- [ ] Implement query history sidebar
- [ ] Add training data management UI
- [ ] Bilingual support (EN/JP)
- [ ] Dark mode support

**Deliverables**:
- Functional web UI at http://localhost:5000
- All 11 API endpoints working (generate_questions, generate_sql, run_sql, etc.)
- Cache-based state management
- Detomo branding (logo, colors, footer)
- Interactive Plotly charts
- CSV download functionality

---

## 8. SUCCESS CRITERIA

### 8.1 MVP Requirements

1. **Core Functionality**:
   - [ ] Natural language to SQL works via Vanna + Claude Agent SDK
   - [ ] SQL execution returns correct results
   - [ ] Basic visualization (Vanna's Plotly)
   - [ ] Training data loaded in ChromaDB

2. **Quality Metrics**:
   - [ ] SQL accuracy ≥ 75% (on 50 test queries)
   - [ ] Response time < 10s (p95)
   - [ ] No critical bugs

3. **API**:
   - [ ] `/api/v0/query` endpoint functional
   - [ ] Claude Agent SDK endpoint running
   - [ ] Health check endpoints

4. **Data**:
   - [ ] Chinook database connected via Vanna
   - [ ] ≥ 50 Q&A training pairs loaded
   - [ ] All DDL and docs loaded

### 8.2 V1.0 Success Criteria

1. **Accuracy**: ≥ 85% SQL correctness
2. **Performance**: < 5s response time (p95)
3. **User Satisfaction**: ≥ 4/5 rating
4. **Coverage**: Support 100+ query patterns

---

## 9. ADVANTAGES OF THIS ARCHITECTURE

### 9.1 Clear Separation of Concerns

| Component | Responsibility |
|-----------|----------------|
| **Vanna AI** | RAG pipeline, training, DB connection, SQL execution, visualization |
| **Claude Agent SDK** | LLM inference only (receive prompt → return text) |
| **ChromaDB** | Vector storage (managed by Vanna) |
| **Chinook DB** | Data storage (managed by Vanna) |

### 9.2 Key Benefits

✅ **Simple**: Vanna handles complex logic, Agent SDK just does LLM calls
✅ **Modular**: Can swap LLM endpoint easily
✅ **Maintainable**: Use Vanna's proven RAG pipeline instead of reinventing
✅ **Flexible**: Can switch to OpenAI/other LLMs by changing endpoint
✅ **Cost-effective**: Agent SDK endpoint can implement caching, rate limiting

### 9.3 vs. Direct Anthropic API

| Direct Anthropic API | Claude Agent SDK Endpoint |
|---------------------|---------------------------|
| Vanna calls API directly | Vanna calls local endpoint → endpoint calls API |
| Hard to add caching | Easy to add caching layer |
| Hard to monitor usage | Easy to add logging, monitoring |
| Couples Vanna to Anthropic | Decouples via HTTP interface |

---

## 10. EXAMPLE USAGE

### 10.1 Setup and Training

```python
from src.detomo_vanna import DetomoVanna

# 1. Initialize Vanna
vn = DetomoVanna(config={
    "path": "./detomo_vectordb",
    "agent_endpoint": "http://localhost:8000/generate",
    "model": "claude-sonnet-4-5"
})

# 2. Connect to database (Vanna handles this)
vn.connect_to_sqlite("data/chinook.db")

# 3. Train (Vanna stores in ChromaDB)
vn.train(ddl="CREATE TABLE Customer (CustomerId INTEGER PRIMARY KEY, ...)")
vn.train(documentation="Customer table stores customer information...")
vn.train(question="How many customers?", sql="SELECT COUNT(*) FROM Customer")

# 4. Query
sql = vn.generate_sql("顧客は何人いますか？")
print(sql)  # SELECT COUNT(*) FROM Customer

df = vn.run_sql(sql)
print(df)  # Shows count

# 5. Visualize
fig = vn.get_plotly_figure(sql=sql, df=df)
fig.show()
```

### 10.2 API Usage

```bash
# Start Claude Agent SDK endpoint
python claude_agent_server.py &  # Port 8000

# Start Flask API
python app.py &  # Port 5000

# Query via API
curl -X POST http://localhost:5000/api/v0/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How many customers are there?"
  }'

# Response:
{
  "sql": "SELECT COUNT(*) FROM Customer",
  "results": [{"COUNT(*)": 59}],
  "columns": ["COUNT(*)"],
  "visualization": null
}
```

---

## 11. FUTURE ENHANCEMENTS

### 11.1 Phase 2 Features

1. **Caching Layer**: Add Redis cache in Claude Agent SDK endpoint
2. **Multiple LLMs**: Support switching between Claude/GPT-4/etc.
3. **Query Optimization**: Add SQL query optimizer
4. **Advanced Viz**: More chart types, custom templates

### 11.2 Advanced Features

1. **Multi-Database**: Support PostgreSQL, MySQL
2. **User Management**: Multi-user, permissions
3. **Query History**: Save and replay queries
4. **Fine-tuning**: Fine-tune embedding model

---

## 12. RISKS & MITIGATIONS

### Risk 1: Claude API Costs
**Impact**: High
**Mitigation**: Add caching in Claude Agent SDK endpoint, rate limiting

### Risk 2: Agent SDK Endpoint Downtime
**Impact**: High
**Mitigation**: Add health checks, auto-restart, fallback to direct API

### Risk 3: SQL Accuracy < 85%
**Impact**: High
**Mitigation**: More training data, prompt engineering, Vanna's built-in RAG

---

## 13. APPENDICES

### Appendix A: Vanna Methods Used

**Training**:
- `vn.train(ddl="...")` - Add DDL to knowledge base
- `vn.train(documentation="...")` - Add docs
- `vn.train(question="...", sql="...")` - Add Q&A pair

**Querying**:
- `vn.generate_sql(question)` - Generate SQL from NL
- `vn.run_sql(sql)` - Execute SQL, return DataFrame
- `vn.get_plotly_figure(sql, df)` - Generate chart

**Management**:
- `vn.get_training_data()` - List all training data
- `vn.remove_training_data(id)` - Remove training item

### Appendix B: Claude Agent SDK Endpoint Spec

**POST /generate**

Request:
```json
{
  "prompt": "Generate SQL for: How many customers?\n\nSchema: CREATE TABLE Customer...",
  "model": "claude-sonnet-4-5",
  "temperature": 0.1,
  "max_tokens": 2048
}
```

Response:
```json
{
  "text": "SELECT COUNT(*) FROM Customer",
  "model": "claude-sonnet-4-5-20250929",
  "usage": {
    "input_tokens": 245,
    "output_tokens": 12
  }
}
```

---

## DOCUMENT VERSION HISTORY

- **v2.0 (2025-10-26)**: Revised with Vanna + Claude Agent SDK endpoint architecture
- **v1.0 (2025-10-25)**: Initial PRD

---

## APPROVAL

- [ ] Product Owner
- [ ] Tech Lead
- [ ] Stakeholders

---

**END OF PRD**
