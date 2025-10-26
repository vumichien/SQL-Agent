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
