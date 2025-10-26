"""Detomo Vanna Production Class - SQLite version"""
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
    Uses ChromaDB for vector storage and SQLite for database.
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
        """Connect to Chinook SQLite database"""
        db_path = config.get_db_path()
        self.connect_to_sqlite(db_path)
        logger.info(f"Connected to SQLite database: {db_path}")

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
