"""
Core configuration settings for Detomo SQL AI.

Uses pydantic-settings to load configuration from environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App Info
    APP_NAME: str = "Detomo SQL AI"
    VERSION: str = "3.0.0"
    API_V0_PREFIX: str = "/api/v0"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Anthropic API
    ANTHROPIC_API_KEY: str
    CLAUDE_MODEL: str = "claude-sonnet-4-5"
    CLAUDE_TEMPERATURE: float = 0.1
    CLAUDE_MAX_TOKENS: int = 2048

    # Database
    DATABASE_PATH: str = "data/chinook.db"
    VECTOR_DB_PATH: str = "./detomo_vectordb"
    USER_DB_PATH: str = "data/users.db"

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative frontend
        "http://localhost:8000",  # Same origin
        "http://192.168.21.126:5173",  # LAN access
        "http://127.0.0.1:5173",  # Alternative localhost
    ]

    # Model settings
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


# Global settings instance
settings = Settings()
