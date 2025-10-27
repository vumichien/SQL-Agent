"""
Training Script for Chinook Database

This script loads all training data (DDL, documentation, Q&A pairs)
into ChromaDB via the DetomoVanna system.

Usage:
    python scripts/train_chinook.py

Prerequisites:
    - Claude Agent endpoint running on http://localhost:8000
    - Chinook database at data/chinook.db
    - Training data in training_data/chinook/
"""

from src.detomo_vanna import DetomoVanna
import json
from pathlib import Path
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def train_chinook_database():
    """
    Load all training data into Vanna (stored in ChromaDB).

    This function:
    1. Initializes DetomoVanna with ChromaDB persistence
    2. Connects to the Chinook SQLite database
    3. Loads DDL files (table schemas)
    4. Loads documentation files (table descriptions)
    5. Loads Q&A pairs (training examples)
    6. Verifies all data was loaded successfully

    Returns:
        int: Total number of training items loaded into ChromaDB

    Raises:
        FileNotFoundError: If database or training data files not found
        Exception: If training fails
    """

    try:
        logger.info("=" * 60)
        logger.info("DETOMO SQL AI - CHINOOK DATABASE TRAINING")
        logger.info("=" * 60)

        # Initialize Vanna with ChromaDB persistence
        logger.info("\n[1/5] Initializing DetomoVanna...")
        vn = DetomoVanna(config={
            "path": "./detomo_vectordb",
            "client": "persistent",
            "agent_endpoint": "http://localhost:8000/generate",
            "model": "claude-sonnet-4-5"
        })
        logger.info("✓ DetomoVanna initialized")

        # Connect to Chinook database
        logger.info("\n[2/5] Connecting to Chinook database...")
        db_path = "data/chinook.db"
        if not Path(db_path).exists():
            raise FileNotFoundError(f"Database not found: {db_path}")
        vn.connect_to_sqlite(db_path)
        logger.info(f"✓ Connected to {db_path}")

        # Train DDL (Table Schemas)
        logger.info("\n[3/5] Loading DDL files (table schemas)...")
        ddl_dir = Path("training_data/chinook/ddl")
        if not ddl_dir.exists():
            raise FileNotFoundError(f"DDL directory not found: {ddl_dir}")

        ddl_count = 0
        for ddl_file in sorted(ddl_dir.glob("*.sql")):
            with open(ddl_file, 'r', encoding='utf-8') as f:
                ddl_content = f.read()
                vn.train(ddl=ddl_content)
                ddl_count += 1
                logger.info(f"  ✓ {ddl_file.name}")
        logger.info(f"✓ Loaded {ddl_count} DDL files")

        # Train Documentation
        logger.info("\n[4/5] Loading documentation files...")
        doc_dir = Path("training_data/chinook/documentation")
        if not doc_dir.exists():
            raise FileNotFoundError(f"Documentation directory not found: {doc_dir}")

        doc_count = 0
        for doc_file in sorted(doc_dir.glob("*.md")):
            with open(doc_file, 'r', encoding='utf-8') as f:
                doc_content = f.read()
                vn.train(documentation=doc_content)
                doc_count += 1
                logger.info(f"  ✓ {doc_file.name}")
        logger.info(f"✓ Loaded {doc_count} documentation files")

        # Train Q&A Pairs
        logger.info("\n[5/5] Loading Q&A pairs...")
        qa_dir = Path("training_data/chinook/questions")
        if not qa_dir.exists():
            raise FileNotFoundError(f"Questions directory not found: {qa_dir}")

        total_pairs = 0
        for qa_file in sorted(qa_dir.glob("*.json")):
            with open(qa_file, 'r', encoding='utf-8') as f:
                qa_pairs = json.load(f)
                for pair in qa_pairs:
                    if "question" not in pair or "sql" not in pair:
                        logger.warning(f"Skipping invalid pair in {qa_file.name}")
                        continue
                    vn.train(
                        question=pair["question"],
                        sql=pair["sql"]
                    )
                    total_pairs += 1
                logger.info(f"  ✓ {qa_file.name}: {len(qa_pairs)} pairs")
        logger.info(f"✓ Loaded {total_pairs} Q&A pairs")

        # Verify training data
        logger.info("\n" + "=" * 60)
        logger.info("VERIFICATION")
        logger.info("=" * 60)
        training_data = vn.get_training_data()
        total_items = len(training_data)

        logger.info(f"DDL files:          {ddl_count}")
        logger.info(f"Documentation:      {doc_count}")
        logger.info(f"Q&A pairs:          {total_pairs}")
        logger.info(f"Total items in DB:  {total_items}")

        logger.info("\n" + "=" * 60)
        logger.info("✅ TRAINING COMPLETED SUCCESSFULLY!")
        logger.info("=" * 60)

        return total_items

    except FileNotFoundError as e:
        logger.error(f"❌ File not found: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Training failed: {e}")
        sys.exit(1)


def verify_training():
    """
    Verify that training data exists in ChromaDB.

    Returns:
        bool: True if training data exists, False otherwise
    """
    try:
        vn = DetomoVanna(config={"path": "./detomo_vectordb"})
        training_data = vn.get_training_data()
        count = len(training_data)

        if count > 0:
            logger.info(f"✓ Training data verified: {count} items in ChromaDB")
            return True
        else:
            logger.warning("⚠ No training data found in ChromaDB")
            return False

    except Exception as e:
        logger.error(f"❌ Verification failed: {e}")
        return False


if __name__ == "__main__":
    train_chinook_database()
