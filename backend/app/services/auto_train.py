"""
Auto-training service for loading training data on startup.

Automatically loads training data from filesystem into ChromaDB
if the database is empty.
"""

import logging
import json
from pathlib import Path
from typing import Optional
from src.detomo_vanna import DetomoVanna

logger = logging.getLogger(__name__)


def auto_load_training_data(vn: DetomoVanna, force: bool = False) -> int:
    """
    Automatically load training data if ChromaDB is empty.
    
    Args:
        vn: DetomoVanna instance
        force: Force reload even if data exists
    
    Returns:
        int: Number of training items loaded
    """
    try:
        # Check existing data
        existing_data = vn.get_training_data()
        existing_count = len(existing_data)
        
        if existing_count > 0 and not force:
            logger.info(f"✓ Training data already exists ({existing_count} items)")
            return existing_count
        
        logger.info("=" * 60)
        logger.info("AUTO-LOADING TRAINING DATA")
        logger.info("=" * 60)
        
        total_loaded = 0
        
        # Load DDL files
        ddl_dir = Path("training_data/chinook/ddl")
        if ddl_dir.exists():
            logger.info(f"\n[1/3] Loading DDL files...")
            ddl_count = 0
            for ddl_file in sorted(ddl_dir.glob("*.sql")):
                try:
                    with open(ddl_file, 'r', encoding='utf-8') as f:
                        ddl_content = f.read()
                        vn.train(ddl=ddl_content)
                        ddl_count += 1
                        logger.info(f"  ✓ {ddl_file.name}")
                except Exception as e:
                    logger.error(f"  ✗ Failed to load {ddl_file.name}: {e}")
            
            logger.info(f"✓ Loaded {ddl_count} DDL files")
            total_loaded += ddl_count
        else:
            logger.warning(f"DDL directory not found: {ddl_dir}")
        
        # Load Documentation files
        doc_dir = Path("training_data/chinook/documentation")
        if doc_dir.exists():
            logger.info(f"\n[2/3] Loading documentation files...")
            doc_count = 0
            for doc_file in sorted(doc_dir.glob("*.md")):
                try:
                    with open(doc_file, 'r', encoding='utf-8') as f:
                        doc_content = f.read()
                        vn.train(documentation=doc_content)
                        doc_count += 1
                        logger.info(f"  ✓ {doc_file.name}")
                except Exception as e:
                    logger.error(f"  ✗ Failed to load {doc_file.name}: {e}")
            
            logger.info(f"✓ Loaded {doc_count} documentation files")
            total_loaded += doc_count
        else:
            logger.warning(f"Documentation directory not found: {doc_dir}")
        
        # Load Q&A pairs
        qa_dir = Path("training_data/chinook/questions")
        if qa_dir.exists():
            logger.info(f"\n[3/3] Loading Q&A pairs...")
            qa_count = 0
            for qa_file in sorted(qa_dir.glob("*.json")):
                try:
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
                            qa_count += 1
                        logger.info(f"  ✓ {qa_file.name}: {len(qa_pairs)} pairs")
                except Exception as e:
                    logger.error(f"  ✗ Failed to load {qa_file.name}: {e}")
            
            logger.info(f"✓ Loaded {qa_count} Q&A pairs")
            total_loaded += qa_count
        else:
            logger.warning(f"Questions directory not found: {qa_dir}")
        
        # Verify
        logger.info("\n" + "=" * 60)
        final_data = vn.get_training_data()
        final_count = len(final_data)
        logger.info(f"✅ AUTO-LOAD COMPLETE: {final_count} items in database")
        logger.info("=" * 60)
        
        return final_count
        
    except Exception as e:
        logger.error(f"❌ Auto-load training data failed: {e}")
        return 0

