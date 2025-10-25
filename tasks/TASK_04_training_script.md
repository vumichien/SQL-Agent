# Task 04: Training Script Implementation

**Priority**: HIGH
**Assignee**: AI Engineer
**Estimate**: 4 hours
**Phase**: Phase 1 - Foundation

---

## Objective
Tạo script để load tất cả training data (DDL, Documentation, Q&A pairs) vào Vanna vector database.

---

## Prerequisites
- Task 02 completed (Training data files ready)
- Task 03 completed (DetomoVanna class implemented)
- All training data files in `training_data/chinook/`

---

## Steps

### Step 1: Create Scripts Directory (5 min)
```bash
mkdir -p scripts
touch scripts/__init__.py
touch scripts/train_chinook.py
```

### Step 2: Implement Training Script (2 hours)

**File: `scripts/train_chinook.py`**
```python
#!/usr/bin/env python3
"""
Training script for Chinook database.
Loads DDL, documentation, and Q&A pairs into Vanna vector database.
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.detomo_vanna_dev import create_vanna_dev
from src.config import config
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ChinookTrainer:
    """Handles training data loading for Chinook database"""

    def __init__(self, vn):
        self.vn = vn
        self.training_dir = config.TRAINING_DATA_DIR
        self.stats = {
            "ddl": 0,
            "documentation": 0,
            "questions": 0,
            "errors": []
        }

    def train_ddl(self):
        """Load DDL files"""
        logger.info("=" * 60)
        logger.info("STEP 1: Training DDL")
        logger.info("=" * 60)

        ddl_dir = self.training_dir / "ddl"
        if not ddl_dir.exists():
            logger.error(f"DDL directory not found: {ddl_dir}")
            return

        ddl_files = sorted(ddl_dir.glob("*.sql"))
        logger.info(f"Found {len(ddl_files)} DDL files")

        for ddl_file in ddl_files:
            try:
                with open(ddl_file, 'r', encoding='utf-8') as f:
                    ddl_content = f.read()

                    # Train
                    self.vn.train(ddl=ddl_content)
                    self.stats["ddl"] += 1

                    logger.info(f"✓ Trained: {ddl_file.name}")
            except Exception as e:
                error_msg = f"Failed to train {ddl_file.name}: {str(e)}"
                logger.error(error_msg)
                self.stats["errors"].append(error_msg)

        logger.info(f"\nDDL Training Complete: {self.stats['ddl']} files")

    def train_documentation(self):
        """Load documentation files"""
        logger.info("\n" + "=" * 60)
        logger.info("STEP 2: Training Documentation")
        logger.info("=" * 60)

        doc_dir = self.training_dir / "documentation"
        if not doc_dir.exists():
            logger.error(f"Documentation directory not found: {doc_dir}")
            return

        doc_files = sorted(doc_dir.glob("*.md"))
        logger.info(f"Found {len(doc_files)} documentation files")

        for doc_file in doc_files:
            try:
                with open(doc_file, 'r', encoding='utf-8') as f:
                    doc_content = f.read()

                    # Train
                    self.vn.train(documentation=doc_content)
                    self.stats["documentation"] += 1

                    logger.info(f"✓ Trained: {doc_file.name}")
            except Exception as e:
                error_msg = f"Failed to train {doc_file.name}: {str(e)}"
                logger.error(error_msg)
                self.stats["errors"].append(error_msg)

        logger.info(f"\nDocumentation Training Complete: {self.stats['documentation']} files")

    def train_questions(self):
        """Load Q&A pairs"""
        logger.info("\n" + "=" * 60)
        logger.info("STEP 3: Training Questions")
        logger.info("=" * 60)

        qa_dir = self.training_dir / "questions"
        if not qa_dir.exists():
            logger.error(f"Questions directory not found: {qa_dir}")
            return

        qa_files = sorted(qa_dir.glob("*.json"))
        logger.info(f"Found {len(qa_files)} Q&A files")

        for qa_file in qa_files:
            try:
                with open(qa_file, 'r', encoding='utf-8') as f:
                    qa_pairs = json.load(f)

                    logger.info(f"\nProcessing: {qa_file.name}")
                    logger.info(f"Questions: {len(qa_pairs)}")

                    for i, pair in enumerate(qa_pairs, 1):
                        try:
                            question = pair.get("question", "")
                            sql = pair.get("sql", "")

                            if not question or not sql:
                                logger.warning(f"  Skipping incomplete pair #{i}")
                                continue

                            # Train
                            self.vn.train(question=question, sql=sql)
                            self.stats["questions"] += 1

                            if i <= 3:  # Show first 3 examples
                                logger.info(f"  ✓ Q: {question[:60]}...")

                        except Exception as e:
                            error_msg = f"Failed to train question #{i} in {qa_file.name}: {str(e)}"
                            logger.error(f"  ✗ {error_msg}")
                            self.stats["errors"].append(error_msg)

                    logger.info(f"✓ Completed: {qa_file.name}")

            except Exception as e:
                error_msg = f"Failed to process {qa_file.name}: {str(e)}"
                logger.error(error_msg)
                self.stats["errors"].append(error_msg)

        logger.info(f"\nQ&A Training Complete: {self.stats['questions']} pairs")

    def verify_training(self):
        """Verify training data was loaded correctly"""
        logger.info("\n" + "=" * 60)
        logger.info("STEP 4: Verification")
        logger.info("=" * 60)

        try:
            training_stats = self.vn.get_training_stats()

            logger.info("\nTraining Data Summary:")
            logger.info(f"  Total items: {training_stats['total']}")
            logger.info(f"  DDL: {training_stats['ddl']}")
            logger.info(f"  Documentation: {training_stats['documentation']}")
            logger.info(f"  SQL/Q&A: {training_stats['sql']}")

            # Test SQL generation
            logger.info("\nTesting SQL Generation:")
            test_questions = [
                "How many customers are there?",
                "List all genres",
                "Top 5 customers by revenue"
            ]

            for question in test_questions:
                try:
                    logger.info(f"\n  Question: {question}")
                    sql = self.vn.generate_sql(question)
                    logger.info(f"  Generated SQL: {sql[:100]}...")
                except Exception as e:
                    logger.warning(f"  Failed: {str(e)}")

        except Exception as e:
            logger.error(f"Verification failed: {str(e)}")

    def print_summary(self):
        """Print training summary"""
        logger.info("\n" + "=" * 60)
        logger.info("TRAINING SUMMARY")
        logger.info("=" * 60)

        logger.info(f"\n✅ Successfully trained:")
        logger.info(f"   DDL files: {self.stats['ddl']}")
        logger.info(f"   Documentation files: {self.stats['documentation']}")
        logger.info(f"   Q&A pairs: {self.stats['questions']}")
        logger.info(f"   Total: {sum([self.stats['ddl'], self.stats['documentation'], self.stats['questions']])}")

        if self.stats["errors"]:
            logger.warning(f"\n⚠️  Errors encountered: {len(self.stats['errors'])}")
            for error in self.stats["errors"][:5]:  # Show first 5 errors
                logger.warning(f"   - {error}")
            if len(self.stats["errors"]) > 5:
                logger.warning(f"   ... and {len(self.stats['errors']) - 5} more")
        else:
            logger.info("\n✅ No errors encountered!")

        logger.info("\n" + "=" * 60)


def main():
    """Main training function"""
    logger.info("Detomo SQL AI - Chinook Training Script")
    logger.info("=" * 60)

    # Initialize Vanna
    logger.info("Initializing Vanna...")
    try:
        vn = create_vanna_dev()
        logger.info("✓ Vanna initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Vanna: {str(e)}")
        sys.exit(1)

    # Create trainer
    trainer = ChinookTrainer(vn)

    # Run training
    try:
        trainer.train_ddl()
        trainer.train_documentation()
        trainer.train_questions()
        trainer.verify_training()
        trainer.print_summary()

        logger.info("\n✅ Training completed successfully!")
        logger.info("You can now use the trained model to generate SQL queries.")

    except KeyboardInterrupt:
        logger.warning("\n\n⚠️  Training interrupted by user")
        trainer.print_summary()
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n\n❌ Training failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
```

### Step 3: Create Helper Scripts (1 hour)

**File: `scripts/reset_training.py`**
```python
#!/usr/bin/env python3
"""
Reset training data - removes all trained data from vector database.
"""

import sys
from pathlib import Path
import shutil
import logging

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def reset_training():
    """Remove vector database to reset training"""
    vector_db_path = Path(config.VECTOR_DB_PATH)

    if vector_db_path.exists():
        logger.warning(f"Removing vector database: {vector_db_path}")
        response = input("Are you sure? This cannot be undone. (yes/no): ")

        if response.lower() == "yes":
            shutil.rmtree(vector_db_path)
            logger.info("✓ Vector database removed successfully")
            logger.info("Run train_chinook.py to retrain")
        else:
            logger.info("Reset cancelled")
    else:
        logger.info(f"Vector database not found: {vector_db_path}")
        logger.info("Nothing to reset")


if __name__ == "__main__":
    reset_training()
```

**File: `scripts/check_training.py`**
```python
#!/usr/bin/env python3
"""
Check current training data statistics.
"""

import sys
from pathlib import Path
import logging

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.detomo_vanna_dev import create_vanna_dev

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_training():
    """Check training data statistics"""
    try:
        vn = create_vanna_dev()
        stats = vn.get_training_stats()

        logger.info("=" * 60)
        logger.info("TRAINING DATA STATISTICS")
        logger.info("=" * 60)
        logger.info(f"Total items: {stats['total']}")
        logger.info(f"DDL: {stats['ddl']}")
        logger.info(f"Documentation: {stats['documentation']}")
        logger.info(f"SQL/Q&A: {stats['sql']}")
        logger.info("=" * 60)

        if stats['total'] == 0:
            logger.warning("No training data found. Run train_chinook.py first.")

    except Exception as e:
        logger.error(f"Failed to check training: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    check_training()
```

### Step 4: Make Scripts Executable (5 min)
```bash
chmod +x scripts/train_chinook.py
chmod +x scripts/reset_training.py
chmod +x scripts/check_training.py
```

### Step 5: Run Training (1 hour)
```bash
# Run training
python scripts/train_chinook.py

# Check stats
python scripts/check_training.py
```

---

## Verification Checklist

### Scripts Created
- [ ] scripts/train_chinook.py
- [ ] scripts/reset_training.py
- [ ] scripts/check_training.py
- [ ] All scripts are executable

### Training Execution
- [ ] Script runs without errors
- [ ] All DDL files loaded
- [ ] All documentation files loaded
- [ ] All Q&A pairs loaded
- [ ] Verification tests pass
- [ ] Summary shows correct counts

### Data Validation
- [ ] Vector database created (detomo_vectordb/)
- [ ] Training stats show expected counts:
  - DDL: ~12 items
  - Documentation: ~11 items
  - Q&A: 70+ pairs
- [ ] Can generate SQL for test questions
- [ ] Generated SQL is syntactically correct

---

## Expected Output

```
Detomo SQL AI - Chinook Training Script
============================================================
Initializing Vanna...
✓ Vanna initialized successfully
Connected to database: chinook

============================================================
STEP 1: Training DDL
============================================================
Found 12 DDL files
✓ Trained: album.sql
✓ Trained: artist.sql
✓ Trained: customer.sql
...
DDL Training Complete: 12 files

============================================================
STEP 2: Training Documentation
============================================================
Found 11 documentation files
✓ Trained: album.md
✓ Trained: artist.md
...
Documentation Training Complete: 11 files

============================================================
STEP 3: Training Questions
============================================================
Found 4 Q&A files

Processing: basic_queries.json
Questions: 20
  ✓ Q: How many customers are there?...
  ✓ Q: 顧客は何人いますか？...
  ✓ Q: List first 10 customers...
✓ Completed: basic_queries.json
...
Q&A Training Complete: 70 pairs

============================================================
STEP 4: Verification
============================================================

Training Data Summary:
  Total items: 93
  DDL: 12
  Documentation: 11
  SQL/Q&A: 70

Testing SQL Generation:

  Question: How many customers are there?
  Generated SQL: SELECT COUNT(*) FROM Customer...

============================================================
TRAINING SUMMARY
============================================================

✅ Successfully trained:
   DDL files: 12
   Documentation files: 11
   Q&A pairs: 70
   Total: 93

✅ No errors encountered!

============================================================

✅ Training completed successfully!
You can now use the trained model to generate SQL queries.
```

---

## Output/Deliverables

- ✅ scripts/train_chinook.py - Main training script
- ✅ scripts/reset_training.py - Reset utility
- ✅ scripts/check_training.py - Stats checker
- ✅ Vector database populated with training data
- ✅ Training logs showing success
- ✅ SQL generation working

---

## Next Task
➡️ [Task 05: Flask API Development](TASK_05_flask_api.md)

---

## Troubleshooting

### Issue: FileNotFoundError for training data
**Solution**: Make sure Task 02 is completed and files exist
```bash
ls -R training_data/chinook/
```

### Issue: Encoding errors with Japanese characters
**Solution**: Ensure UTF-8 encoding
```python
open(file, 'r', encoding='utf-8')
```

### Issue: Training takes very long
**Solution**: This is normal for first training. Vector embeddings take time.
- Expected time: 5-10 minutes for 90+ items

### Issue: SQL generation fails after training
**Solution**: Check that database connection is working
```python
vn.run_sql("SELECT 1")
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
