"""Configuration for Detomo SQL AI"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""

    # App
    APP_NAME = "Detomo SQL AI"
    VERSION = "1.0.0"

    # Database (SQLite)
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")
    DB_PATH = os.getenv("DB_PATH", "data/chinook.db")

    # LLM Backend
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    LLM_BACKEND = os.getenv("LLM_BACKEND", "claude_agent_sdk")  # or "anthropic_api"
    LLM_MODEL = os.getenv("LLM_MODEL", "claude-3-5-sonnet-20241022")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2048"))

    # Vector DB
    VECTOR_DB_PATH = "./detomo_vectordb"
    EMBEDDING_MODEL = "BAAI/bge-m3"
    N_RESULTS = 10

    # Training Data
    TRAINING_DATA_DIR = Path("training_data/chinook")

    @classmethod
    def get_db_path(cls):
        """Get SQLite database path"""
        return cls.DB_PATH

    @classmethod
    def get_llm_config(cls):
        """Get LLM configuration dictionary"""
        return {
            "model": cls.LLM_MODEL,
            "temperature": cls.LLM_TEMPERATURE,
            "max_tokens": cls.LLM_MAX_TOKENS,
        }


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENV = "development"
    LOG_LEVEL = "INFO"


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENV = "production"
    LOG_LEVEL = "WARNING"


# Default config
config = DevelopmentConfig()
