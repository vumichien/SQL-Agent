"""
Database utilities for user management.

Uses SQLite for storing user accounts.
"""

import sqlite3
from pathlib import Path
from typing import Optional
from ..core.config import settings


class Database:
    """Database manager for user data."""

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database connection.

        Args:
            db_path (str, optional): Path to SQLite database file
        """
        self.db_path = db_path or settings.USER_DB_PATH
        self._init_db()

    def _init_db(self):
        """Initialize database schema (create tables if not exist)."""
        # Ensure parent directory exists
        db_file = Path(self.db_path)
        db_file.parent.mkdir(parents=True, exist_ok=True)

        # Create connection and tables
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create indexes for faster lookups
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_email
            ON users(email)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_username
            ON users(username)
        """)

        conn.commit()
        conn.close()

    def get_connection(self) -> sqlite3.Connection:
        """
        Get a new database connection.

        Returns:
            sqlite3.Connection: Database connection

        Example:
            >>> db = Database()
            >>> conn = db.get_connection()
            >>> cursor = conn.cursor()
            >>> cursor.execute("SELECT * FROM users")
            >>> conn.close()
        """
        return sqlite3.connect(self.db_path)

    def close_all_connections(self):
        """Close all database connections (for testing)."""
        # SQLite doesn't maintain persistent connections, so this is a no-op
        pass


# Global database instance
_db_instance: Optional[Database] = None


def get_db() -> Database:
    """
    Get the global database instance (singleton pattern).

    Returns:
        Database: The database instance
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance
