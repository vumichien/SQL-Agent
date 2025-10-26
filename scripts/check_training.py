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
