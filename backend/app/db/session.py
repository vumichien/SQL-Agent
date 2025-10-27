"""
Database session management utilities.

Provides context managers and utilities for database transactions.
"""

from contextlib import contextmanager
import sqlite3
from typing import Generator
from .base import get_db


@contextmanager
def get_db_session() -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager for database sessions with automatic commit/rollback.

    Yields:
        sqlite3.Connection: Database connection

    Example:
        >>> with get_db_session() as conn:
        ...     cursor = conn.cursor()
        ...     cursor.execute("INSERT INTO users ...")
        ...     # Automatically commits on success, rolls back on error
    """
    db = get_db()
    conn = db.get_connection()

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def execute_query(query: str, params: tuple = ()) -> list:
    """
    Execute a SELECT query and return results.

    Args:
        query (str): SQL query to execute
        params (tuple): Query parameters

    Returns:
        list: Query results

    Example:
        >>> results = execute_query(
        ...     "SELECT * FROM users WHERE username = ?",
        ...     ("john",)
        ... )
    """
    with get_db_session() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()


def execute_update(query: str, params: tuple = ()) -> int:
    """
    Execute an INSERT/UPDATE/DELETE query.

    Args:
        query (str): SQL query to execute
        params (tuple): Query parameters

    Returns:
        int: Number of affected rows or last row ID for INSERT

    Example:
        >>> row_id = execute_update(
        ...     "INSERT INTO users (username, email) VALUES (?, ?)",
        ...     ("john", "john@example.com")
        ... )
    """
    with get_db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.lastrowid if cursor.lastrowid else cursor.rowcount
