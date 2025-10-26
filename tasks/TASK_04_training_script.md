# TASK 04: Training Script

**Status**: ⬜ Not Started
**Estimated Time**: 4-6 hours
**Dependencies**: TASK 02 (DetomoVanna), TASK 03 (Training data)
**Phase**: 2 - Training Data & Knowledge Base

---

## OVERVIEW

Create script to load all training data (DDL, documentation, Q&A pairs) into ChromaDB via Vanna.

**Reference**: PRD Section 4.4

---

## OBJECTIVES

1. Create `scripts/train_chinook.py`
2. Load DDL files into Vanna
3. Load documentation into Vanna
4. Load Q&A pairs into Vanna
5. Verify training data loaded
6. Create integration tests

---

## IMPLEMENTATION

Create `scripts/train_chinook.py`:

```python
from src.detomo_vanna import DetomoVanna
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train_chinook_database():
    """Load training data into Vanna (stored in ChromaDB)."""

    # Initialize Vanna
    vn = DetomoVanna(config={
        "path": "./detomo_vectordb",
        "client": "persistent",
        "agent_endpoint": "http://localhost:8000/generate",
        "model": "claude-sonnet-4-5"
    })

    # Connect to database
    vn.connect_to_sqlite("data/chinook.db")

    # 1. Train DDL
    logger.info("Training DDL...")
    ddl_dir = Path("training_data/chinook/ddl")
    for ddl_file in sorted(ddl_dir.glob("*.sql")):
        with open(ddl_file, 'r', encoding='utf-8') as f:
            ddl_content = f.read()
            vn.train(ddl=ddl_content)
            logger.info(f"✓ Trained {ddl_file.name}")

    # 2. Train Documentation
    logger.info("\nTraining Documentation...")
    doc_dir = Path("training_data/chinook/documentation")
    for doc_file in sorted(doc_dir.glob("*.md")):
        with open(doc_file, 'r', encoding='utf-8') as f:
            doc_content = f.read()
            vn.train(documentation=doc_content)
            logger.info(f"✓ Trained {doc_file.name}")

    # 3. Train Q&A Pairs
    logger.info("\nTraining Questions...")
    qa_dir = Path("training_data/chinook/questions")
    total_pairs = 0
    for qa_file in sorted(qa_dir.glob("*.json")):
        with open(qa_file, 'r', encoding='utf-8') as f:
            qa_pairs = json.load(f)
            for pair in qa_pairs:
                vn.train(
                    question=pair["question"],
                    sql=pair["sql"]
                )
                total_pairs += 1
            logger.info(f"✓ Trained {len(qa_pairs)} pairs from {qa_file.name}")

    logger.info(f"\n✅ Training completed! Total Q&A pairs: {total_pairs}")

    # Verify training data
    training_data = vn.get_training_data()
    logger.info(f"Total training items in ChromaDB: {len(training_data)}")

    return len(training_data)


if __name__ == "__main__":
    train_chinook_database()
```

---

## SUCCESS CRITERIA

- [ ] `scripts/train_chinook.py` created
- [ ] Script loads all DDL files
- [ ] Script loads all documentation
- [ ] Script loads all Q&A pairs
- [ ] ChromaDB folder created (`detomo_vectordb/`)
- [ ] Can verify training data count
- [ ] Script is idempotent (can re-run safely)
- [ ] Integration test passing

---

## TESTING

```bash
# Start Claude Agent endpoint first
python claude_agent_server.py

# Run training script
python scripts/train_chinook.py

# Verify ChromaDB folder exists
ls detomo_vectordb/
```

Create `tests/integration/test_training.py`:

```python
import pytest
from scripts.train_chinook import train_chinook_database
from src.detomo_vanna import DetomoVanna


def test_training_script():
    """Test training script loads data successfully"""
    count = train_chinook_database()
    assert count >= 50  # At least 50 training items


def test_training_data_retrievable():
    """Test can retrieve training data after loading"""
    vn = DetomoVanna(config={"path": "./detomo_vectordb"})
    training_data = vn.get_training_data()
    assert len(training_data) > 0
```

---

## REFERENCES

- **PRD Section 4.4**: Training Data Management

---

**Last Updated**: 2025-10-26
