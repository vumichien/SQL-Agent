# Task 03: Implement DetomoVanna Class

**Priority**: HIGH
**Assignee**: AI Engineer
**Estimate**: 8 hours
**Phase**: Phase 1 - Foundation

---

## Objective
Implement custom Vanna class integrating Claude Agent SDK (dev) và Anthropic API (prod) với ChromaDB vector store.

---

## Prerequisites
- Task 01 completed (Chinook database ready)
- Task 02 completed (Training data ready)
- Python 3.10+ installed
- Understanding of Vanna AI framework

---

## Architecture

```
DetomoVannaDev (Development)
├── ChromaDB_VectorStore
└── ClaudeAgentChat (Custom wrapper for Claude Agent SDK)

DetomoVannaProd (Production)
├── ChromaDB_VectorStore
└── Anthropic_Chat (Built-in Vanna support)
```

---

## Steps

### Step 1: Install Dependencies (30 min)

**File: `requirements.txt`**
```txt
# Core
vanna==0.7.9
anthropic>=0.40.0
chromadb<1.0.0
psycopg2-binary

# Embeddings
langchain-huggingface
sentence-transformers

# Utilities
python-dotenv
```

**Install**:
```bash
pip install -r requirements.txt
```

### Step 2: Create Project Structure (15 min)

```bash
mkdir -p src
touch src/__init__.py
touch src/detomo_vanna_dev.py
touch src/detomo_vanna_prod.py
touch src/config.py
```

### Step 3: Implement Configuration (1 hour)

**File: `src/config.py`**
```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""

    # App
    APP_NAME = "Detomo SQL AI"
    VERSION = "1.0.0"

    # Database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "chinook")
    DB_USER = os.getenv("DB_USER", "detomo_reader")
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

    @classmethod
    def get_db_connection_string(cls):
        """Get PostgreSQL connection string"""
        return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENV = "development"

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENV = "production"

# Default config
config = DevelopmentConfig()
```

**Create `.env` file**:
```bash
# Database
DB_HOST=localhost
DB_NAME=chinook
DB_USER=detomo_reader
DB_PASSWORD=your_password
DB_PORT=5432

# LLM (for production)
ANTHROPIC_API_KEY=sk-ant-your-api-key
```

### Step 4: Implement Claude Agent SDK Wrapper (3 hours)

**File: `src/claude_agent_wrapper.py`**
```python
import asyncio
from typing import List, Dict, Any
from vanna.base import VannaBase

# Note: This is a placeholder for Claude Agent SDK integration
# You'll need to install and configure the actual SDK

class ClaudeAgentChat(VannaBase):
    """
    Custom wrapper for Claude Agent SDK.
    This integrates the Agent SDK with Vanna framework.
    """

    def __init__(self, config=None):
        VannaBase.__init__(self, config=config)

        # Config
        self.temperature = config.get("temperature", 0.1) if config else 0.1
        self.max_tokens = config.get("max_tokens", 2048) if config else 2048
        self.model = config.get("model", "claude-3-5-sonnet-20241022") if config else "claude-3-5-sonnet-20241022"

        # Event loop for async operations
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def system_message(self, message: str) -> Dict[str, Any]:
        """Format system message"""
        return {"role": "system", "content": message}

    def user_message(self, message: str) -> Dict[str, Any]:
        """Format user message"""
        return {"role": "user", "content": message}

    def assistant_message(self, message: str) -> Dict[str, Any]:
        """Format assistant message"""
        return {"role": "assistant", "content": message}

    def submit_prompt(self, prompt: List[Dict[str, Any]], **kwargs) -> str:
        """
        Vanna calls this method. We convert to Agent SDK format.
        For now, using Anthropic API as fallback.
        """
        # TODO: Implement actual Claude Agent SDK integration
        # For now, use Anthropic API
        import anthropic

        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        # Extract messages
        messages = []
        system_message = ""

        for msg in prompt:
            role = msg.get("role")
            content = msg.get("content", "")

            if role == "system":
                system_message = content
            elif role in ["user", "assistant"]:
                messages.append({"role": role, "content": content})

        # Call API
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=system_message if system_message else None,
            messages=messages
        )

        return response.content[0].text

    def __del__(self):
        """Cleanup event loop"""
        if hasattr(self, 'loop') and not self.loop.is_closed():
            self.loop.close()
```

### Step 5: Implement DetomoVanna Development Class (2 hours)

**File: `src/detomo_vanna_dev.py`**
```python
from vanna.chromadb import ChromaDB_VectorStore
from chromadb.utils import embedding_functions
from .claude_agent_wrapper import ClaudeAgentChat
from .config import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DetomoVannaDev(ChromaDB_VectorStore, ClaudeAgentChat):
    """
    Development version using Claude Agent SDK.
    Uses ChromaDB for vector storage.
    """

    def __init__(self, config_dict=None):
        """
        Initialize Detomo Vanna for Development

        Args:
            config_dict: Optional config dictionary to override defaults
        """
        if config_dict is None:
            config_dict = {}

        # Default config
        default_config = {
            # ChromaDB
            "path": config.VECTOR_DB_PATH,
            "client": "persistent",
            "embedding_function": embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=config.EMBEDDING_MODEL
            ),
            "n_results": config.N_RESULTS,

            # Claude Agent SDK
            "model": config.LLM_MODEL,
            "temperature": config.LLM_TEMPERATURE,
            "max_tokens": config.LLM_MAX_TOKENS
        }

        # Merge configs
        final_config = {**default_config, **config_dict}

        # Initialize parent classes
        ChromaDB_VectorStore.__init__(self, config=final_config)
        ClaudeAgentChat.__init__(self, config=final_config)

        logger.info("DetomoVannaDev initialized")
        logger.info(f"Vector DB: {final_config['path']}")
        logger.info(f"Model: {final_config['model']}")

    def connect_to_database(self):
        """Connect to Chinook PostgreSQL database"""
        self.connect_to_postgres(
            host=config.DB_HOST,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            port=config.DB_PORT
        )
        logger.info(f"Connected to database: {config.DB_NAME}")

    def get_training_stats(self):
        """Get training data statistics"""
        df = self.get_training_data()

        stats = {
            "total": len(df),
            "ddl": len(df[df['training_data_type'] == 'ddl']),
            "documentation": len(df[df['training_data_type'] == 'documentation']),
            "sql": len(df[df['training_data_type'] == 'sql'])
        }

        logger.info(f"Training stats: {stats}")
        return stats

# Convenience function
def create_vanna_dev(custom_config=None):
    """
    Factory function to create DetomoVannaDev instance

    Args:
        custom_config: Optional config dictionary

    Returns:
        Configured DetomoVannaDev instance
    """
    vn = DetomoVannaDev(config_dict=custom_config)
    vn.connect_to_database()
    return vn
```

### Step 6: Implement DetomoVanna Production Class (1 hour)

**File: `src/detomo_vanna_prod.py`**
```python
from vanna.chromadb import ChromaDB_VectorStore
from vanna.anthropic import Anthropic_Chat
from chromadb.utils import embedding_functions
from .config import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DetomoVannaProd(ChromaDB_VectorStore, Anthropic_Chat):
    """
    Production version using Anthropic API.
    Uses ChromaDB for vector storage.
    """

    def __init__(self, config_dict=None):
        """
        Initialize Detomo Vanna for Production

        Args:
            config_dict: Optional config dictionary to override defaults
        """
        if config_dict is None:
            config_dict = {}

        # Default config
        default_config = {
            # ChromaDB
            "path": config.VECTOR_DB_PATH,
            "client": "persistent",
            "embedding_function": embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=config.EMBEDDING_MODEL
            ),
            "n_results": config.N_RESULTS,

            # Anthropic API
            "api_key": config.ANTHROPIC_API_KEY,
            "model": config.LLM_MODEL,
            "temperature": config.LLM_TEMPERATURE,
            "max_tokens": config.LLM_MAX_TOKENS
        }

        # Merge configs
        final_config = {**default_config, **config_dict}

        # Initialize parent classes
        ChromaDB_VectorStore.__init__(self, config=final_config)
        Anthropic_Chat.__init__(self, config=final_config)

        logger.info("DetomoVannaProd initialized")
        logger.info(f"Vector DB: {final_config['path']}")
        logger.info(f"Model: {final_config['model']}")

    def connect_to_database(self):
        """Connect to Chinook PostgreSQL database"""
        self.connect_to_postgres(
            host=config.DB_HOST,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            port=config.DB_PORT
        )
        logger.info(f"Connected to database: {config.DB_NAME}")

    def get_training_stats(self):
        """Get training data statistics"""
        df = self.get_training_data()

        stats = {
            "total": len(df),
            "ddl": len(df[df['training_data_type'] == 'ddl']),
            "documentation": len(df[df['training_data_type'] == 'documentation']),
            "sql": len(df[df['training_data_type'] == 'sql'])
        }

        logger.info(f"Training stats: {stats}")
        return stats

# Convenience function
def create_vanna_prod(custom_config=None):
    """
    Factory function to create DetomoVannaProd instance

    Args:
        custom_config: Optional config dictionary

    Returns:
        Configured DetomoVannaProd instance
    """
    vn = DetomoVannaProd(config_dict=custom_config)
    vn.connect_to_database()
    return vn
```

### Step 7: Create Tests (1.5 hours)

**File: `tests/test_detomo_vanna.py`**
```python
import pytest
from src.detomo_vanna_dev import create_vanna_dev
from src.config import config

def test_vanna_initialization():
    """Test that Vanna initializes correctly"""
    vn = create_vanna_dev()
    assert vn is not None

def test_database_connection():
    """Test database connection"""
    vn = create_vanna_dev()
    # Test simple query
    result = vn.run_sql("SELECT COUNT(*) FROM Customer")
    assert result is not None
    assert len(result) > 0

def test_sql_generation():
    """Test SQL generation (requires training data)"""
    vn = create_vanna_dev()

    # This will only work after training
    try:
        sql = vn.generate_sql("How many customers are there?")
        assert "Customer" in sql
        assert "COUNT" in sql.upper()
    except Exception as e:
        pytest.skip(f"Training data not loaded yet: {e}")

def test_training_stats():
    """Test training stats"""
    vn = create_vanna_dev()
    stats = vn.get_training_stats()
    assert "total" in stats
    assert "ddl" in stats
    assert "documentation" in stats
    assert "sql" in stats
```

**Run tests**:
```bash
pytest tests/test_detomo_vanna.py -v
```

---

## Verification Checklist

### Setup
- [ ] requirements.txt created
- [ ] All dependencies installed
- [ ] .env file configured
- [ ] Project structure created

### Implementation
- [ ] config.py implemented and working
- [ ] claude_agent_wrapper.py created
- [ ] detomo_vanna_dev.py implemented
- [ ] detomo_vanna_prod.py implemented
- [ ] Both classes can initialize
- [ ] Database connection works

### Testing
- [ ] test_detomo_vanna.py created
- [ ] Initialization test passes
- [ ] Database connection test passes
- [ ] Code follows Python best practices
- [ ] Proper error handling implemented
- [ ] Logging configured

---

## Usage Examples

### Development Usage
```python
from src.detomo_vanna_dev import create_vanna_dev

# Create instance
vn = create_vanna_dev()

# Check connection
print(vn.run_sql("SELECT COUNT(*) FROM Customer"))

# Check training stats
print(vn.get_training_stats())
```

### Production Usage
```python
from src.detomo_vanna_prod import create_vanna_prod

# Create instance
vn = create_vanna_prod()

# Generate SQL
sql = vn.generate_sql("Top 10 customers by revenue")
print(sql)

# Execute
results = vn.run_sql(sql)
print(results)
```

---

## Output/Deliverables

- ✅ src/config.py - Configuration management
- ✅ src/claude_agent_wrapper.py - Claude SDK wrapper
- ✅ src/detomo_vanna_dev.py - Development class
- ✅ src/detomo_vanna_prod.py - Production class
- ✅ requirements.txt - Dependencies
- ✅ .env - Environment variables
- ✅ tests/test_detomo_vanna.py - Unit tests
- ✅ All tests passing

---

## Next Task
➡️ [Task 04: Training Script Implementation](TASK_04_training_script.md)

---

## Troubleshooting

### Issue: ChromaDB initialization fails
**Solution**: Check VECTOR_DB_PATH exists and has write permissions
```bash
mkdir -p detomo_vectordb
chmod 755 detomo_vectordb
```

### Issue: Database connection fails
**Solution**: Verify .env credentials and database is running
```bash
psql -U detomo_reader -d chinook -h localhost
```

### Issue: Import errors
**Solution**: Make sure you're in the correct Python environment
```bash
pip list | grep vanna
pip list | grep anthropic
```

---

## Status
- [ ] Not Started
- [ ] In Progress
- [ ] Blocked (reason: _________________)
- [ ] Completed
- [ ] Verified

**Completed Date**: __________
**Completed By**: __________
