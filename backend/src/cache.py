"""
Memory Cache Module for Detomo SQL AI

This module provides an in-memory cache for storing query state across API calls,
following the vanna-flask pattern. It enables multi-step workflows where SQL generation,
execution, and visualization can be done in separate API calls.

Author: Detomo SQL AI Team
Created: 2025-10-26
"""

import uuid
from typing import Any, Dict, List, Optional


class MemoryCache:
    """
    In-memory cache for storing query state across API calls.

    This cache is used to store intermediate query results including:
    - question: Natural language question
    - sql: Generated SQL query
    - df: Query results as DataFrame
    - fig: Plotly figure JSON
    - error: Error messages if any

    Example:
        >>> cache = MemoryCache()
        >>> cache_id = cache.generate_id()
        >>> cache.set(cache_id, "question", "How many customers?")
        >>> cache.get(cache_id, "question")
        'How many customers?'
    """

    def __init__(self):
        """Initialize empty cache dictionary."""
        self.cache: Dict[str, Dict[str, Any]] = {}

    def generate_id(self) -> str:
        """
        Generate unique ID for cache entry.

        Returns:
            str: UUID4 string

        Example:
            >>> cache = MemoryCache()
            >>> id1 = cache.generate_id()
            >>> id2 = cache.generate_id()
            >>> id1 != id2
            True
        """
        return str(uuid.uuid4())

    def set(self, id: str, field: str, value: Any) -> None:
        """
        Set a field for a specific ID.

        If the ID doesn't exist, creates a new cache entry.
        If the ID exists, updates or adds the field.

        Args:
            id (str): Cache entry ID
            field (str): Field name (e.g., "question", "sql", "df", "fig")
            value (Any): Value to store

        Example:
            >>> cache = MemoryCache()
            >>> cache_id = cache.generate_id()
            >>> cache.set(cache_id, "question", "How many customers?")
            >>> cache.set(cache_id, "sql", "SELECT COUNT(*) FROM customers")
        """
        if id not in self.cache:
            self.cache[id] = {}
        self.cache[id][field] = value

    def get(self, id: str, field: str) -> Optional[Any]:
        """
        Get a field for a specific ID.

        Args:
            id (str): Cache entry ID
            field (str): Field name to retrieve

        Returns:
            Optional[Any]: Field value if found, None otherwise

        Example:
            >>> cache = MemoryCache()
            >>> cache_id = cache.generate_id()
            >>> cache.set(cache_id, "question", "How many customers?")
            >>> cache.get(cache_id, "question")
            'How many customers?'
            >>> cache.get(cache_id, "nonexistent")
            None
            >>> cache.get("invalid_id", "question")
            None
        """
        if id not in self.cache:
            return None
        return self.cache[id].get(field)

    def get_all(self, field: str) -> List[Dict[str, Any]]:
        """
        Get all values of a specific field across all cached entries.

        This is useful for retrieving query history or listing all questions.

        Args:
            field (str): Field name to retrieve from all entries

        Returns:
            List[Dict[str, Any]]: List of dicts with "id" and the field value

        Example:
            >>> cache = MemoryCache()
            >>> id1 = cache.generate_id()
            >>> id2 = cache.generate_id()
            >>> cache.set(id1, "question", "Q1")
            >>> cache.set(id2, "question", "Q2")
            >>> cache.get_all("question")
            [{'id': '...', 'question': 'Q1'}, {'id': '...', 'question': 'Q2'}]
        """
        result = []
        for cache_id, cache_data in self.cache.items():
            if field in cache_data:
                result.append({"id": cache_id, field: cache_data[field]})
        return result

    def delete(self, id: str) -> bool:
        """
        Delete entire cache entry by ID.

        Args:
            id (str): Cache entry ID to delete

        Returns:
            bool: True if entry was deleted, False if ID not found

        Example:
            >>> cache = MemoryCache()
            >>> cache_id = cache.generate_id()
            >>> cache.set(cache_id, "question", "Test")
            >>> cache.delete(cache_id)
            True
            >>> cache.get(cache_id, "question")
            None
            >>> cache.delete("nonexistent_id")
            False
        """
        if id in self.cache:
            del self.cache[id]
            return True
        return False

    def clear(self) -> None:
        """
        Clear all cache entries.

        This is useful for testing or resetting the cache.

        Example:
            >>> cache = MemoryCache()
            >>> cache_id = cache.generate_id()
            >>> cache.set(cache_id, "question", "Test")
            >>> cache.clear()
            >>> cache.get(cache_id, "question")
            None
        """
        self.cache.clear()

    def size(self) -> int:
        """
        Get the number of cache entries.

        Returns:
            int: Number of cache entries

        Example:
            >>> cache = MemoryCache()
            >>> cache.size()
            0
            >>> cache_id = cache.generate_id()
            >>> cache.set(cache_id, "question", "Test")
            >>> cache.size()
            1
        """
        return len(self.cache)

    def exists(self, id: str) -> bool:
        """
        Check if a cache entry exists.

        Args:
            id (str): Cache entry ID to check

        Returns:
            bool: True if entry exists, False otherwise

        Example:
            >>> cache = MemoryCache()
            >>> cache_id = cache.generate_id()
            >>> cache.exists(cache_id)
            False
            >>> cache.set(cache_id, "question", "Test")
            >>> cache.exists(cache_id)
            True
        """
        return id in self.cache
