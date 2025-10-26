"""
Unit Tests for Cache Module

Tests the MemoryCache class functionality including:
- ID generation
- Setting and getting cache values
- Retrieving all values for a field
- Deleting cache entries
- Additional utility methods (clear, size, exists)

Author: Detomo SQL AI Team
Created: 2025-10-26
"""

import pytest
from src.cache import MemoryCache


class TestMemoryCache:
    """Test suite for MemoryCache class."""

    def test_init(self):
        """Test cache initialization."""
        cache = MemoryCache()
        assert cache.cache == {}
        assert cache.size() == 0

    def test_generate_id(self):
        """Test ID generation produces unique UUIDs."""
        cache = MemoryCache()
        id1 = cache.generate_id()
        id2 = cache.generate_id()

        # IDs should be strings
        assert isinstance(id1, str)
        assert isinstance(id2, str)

        # IDs should be unique
        assert id1 != id2

        # IDs should be valid UUIDs (36 characters with hyphens)
        assert len(id1) == 36
        assert len(id2) == 36

    def test_cache_set_and_get(self):
        """Test setting and getting a single field."""
        cache = MemoryCache()
        cache_id = cache.generate_id()

        cache.set(cache_id, "question", "How many customers?")
        result = cache.get(cache_id, "question")

        assert result == "How many customers?"

    def test_cache_set_multiple_fields(self):
        """Test setting multiple fields for the same ID."""
        cache = MemoryCache()
        cache_id = cache.generate_id()

        cache.set(cache_id, "question", "How many customers?")
        cache.set(cache_id, "sql", "SELECT COUNT(*) FROM customers")
        cache.set(cache_id, "df", {"count": 59})

        assert cache.get(cache_id, "question") == "How many customers?"
        assert cache.get(cache_id, "sql") == "SELECT COUNT(*) FROM customers"
        assert cache.get(cache_id, "df") == {"count": 59}

    def test_cache_set_overwrite(self):
        """Test overwriting an existing field."""
        cache = MemoryCache()
        cache_id = cache.generate_id()

        cache.set(cache_id, "question", "Old question")
        cache.set(cache_id, "question", "New question")

        assert cache.get(cache_id, "question") == "New question"

    def test_cache_get_nonexistent_id(self):
        """Test getting a field from a nonexistent ID returns None."""
        cache = MemoryCache()
        result = cache.get("nonexistent_id", "question")
        assert result is None

    def test_cache_get_nonexistent_field(self):
        """Test getting a nonexistent field returns None."""
        cache = MemoryCache()
        cache_id = cache.generate_id()
        cache.set(cache_id, "question", "Test")

        result = cache.get(cache_id, "nonexistent_field")
        assert result is None

    def test_cache_get_all_empty(self):
        """Test get_all on empty cache returns empty list."""
        cache = MemoryCache()
        result = cache.get_all("question")
        assert result == []

    def test_cache_get_all_single_entry(self):
        """Test get_all with single cache entry."""
        cache = MemoryCache()
        id1 = cache.generate_id()
        cache.set(id1, "question", "Q1")

        all_questions = cache.get_all("question")

        assert len(all_questions) == 1
        assert all_questions[0]["id"] == id1
        assert all_questions[0]["question"] == "Q1"

    def test_cache_get_all_multiple_entries(self):
        """Test get_all with multiple cache entries."""
        cache = MemoryCache()
        id1 = cache.generate_id()
        id2 = cache.generate_id()
        id3 = cache.generate_id()

        cache.set(id1, "question", "Q1")
        cache.set(id2, "question", "Q2")
        cache.set(id3, "question", "Q3")

        all_questions = cache.get_all("question")

        assert len(all_questions) == 3

        # Extract questions
        questions = [item["question"] for item in all_questions]
        assert "Q1" in questions
        assert "Q2" in questions
        assert "Q3" in questions

    def test_cache_get_all_partial_field(self):
        """Test get_all when only some entries have the field."""
        cache = MemoryCache()
        id1 = cache.generate_id()
        id2 = cache.generate_id()
        id3 = cache.generate_id()

        cache.set(id1, "question", "Q1")
        cache.set(id2, "question", "Q2")
        cache.set(id3, "sql", "SELECT * FROM test")  # No question field

        all_questions = cache.get_all("question")

        assert len(all_questions) == 2

    def test_cache_get_all_nonexistent_field(self):
        """Test get_all for a field that doesn't exist in any entry."""
        cache = MemoryCache()
        id1 = cache.generate_id()
        cache.set(id1, "question", "Q1")

        result = cache.get_all("nonexistent_field")
        assert result == []

    def test_cache_delete_existing(self):
        """Test deleting an existing cache entry."""
        cache = MemoryCache()
        cache_id = cache.generate_id()

        cache.set(cache_id, "question", "Test")
        result = cache.delete(cache_id)

        assert result is True
        assert cache.get(cache_id, "question") is None
        assert cache.size() == 0

    def test_cache_delete_nonexistent(self):
        """Test deleting a nonexistent cache entry returns False."""
        cache = MemoryCache()
        result = cache.delete("nonexistent_id")
        assert result is False

    def test_cache_delete_multiple_fields(self):
        """Test deleting an entry with multiple fields."""
        cache = MemoryCache()
        cache_id = cache.generate_id()

        cache.set(cache_id, "question", "Q1")
        cache.set(cache_id, "sql", "SELECT * FROM test")
        cache.set(cache_id, "df", {"col1": "val1"})

        cache.delete(cache_id)

        assert cache.get(cache_id, "question") is None
        assert cache.get(cache_id, "sql") is None
        assert cache.get(cache_id, "df") is None

    def test_cache_clear(self):
        """Test clearing all cache entries."""
        cache = MemoryCache()
        id1 = cache.generate_id()
        id2 = cache.generate_id()

        cache.set(id1, "question", "Q1")
        cache.set(id2, "question", "Q2")

        assert cache.size() == 2

        cache.clear()

        assert cache.size() == 0
        assert cache.get(id1, "question") is None
        assert cache.get(id2, "question") is None

    def test_cache_size(self):
        """Test size method returns correct count."""
        cache = MemoryCache()
        assert cache.size() == 0

        id1 = cache.generate_id()
        cache.set(id1, "question", "Q1")
        assert cache.size() == 1

        id2 = cache.generate_id()
        cache.set(id2, "question", "Q2")
        assert cache.size() == 2

        cache.delete(id1)
        assert cache.size() == 1

        cache.clear()
        assert cache.size() == 0

    def test_cache_exists(self):
        """Test exists method."""
        cache = MemoryCache()
        cache_id = cache.generate_id()

        assert cache.exists(cache_id) is False

        cache.set(cache_id, "question", "Test")
        assert cache.exists(cache_id) is True

        cache.delete(cache_id)
        assert cache.exists(cache_id) is False

    def test_cache_workflow(self):
        """Test a realistic multi-step query workflow."""
        cache = MemoryCache()

        # Step 1: Generate SQL
        cache_id = cache.generate_id()
        cache.set(cache_id, "question", "How many customers?")
        cache.set(cache_id, "sql", "SELECT COUNT(*) FROM customers")

        # Step 2: Run SQL
        cache.set(cache_id, "df", {"count": 59})

        # Step 3: Generate visualization
        cache.set(cache_id, "fig", {"data": [], "layout": {}})

        # Verify all steps stored correctly
        assert cache.get(cache_id, "question") == "How many customers?"
        assert cache.get(cache_id, "sql") == "SELECT COUNT(*) FROM customers"
        assert cache.get(cache_id, "df") == {"count": 59}
        assert cache.get(cache_id, "fig") == {"data": [], "layout": {}}

        # Verify size
        assert cache.size() == 1

    def test_cache_multiple_queries(self):
        """Test handling multiple concurrent queries."""
        cache = MemoryCache()

        # Create 3 different queries
        id1 = cache.generate_id()
        id2 = cache.generate_id()
        id3 = cache.generate_id()

        cache.set(id1, "question", "How many customers?")
        cache.set(id2, "question", "List all artists")
        cache.set(id3, "question", "Top 5 albums")

        cache.set(id1, "sql", "SELECT COUNT(*) FROM customers")
        cache.set(id2, "sql", "SELECT * FROM artists")
        cache.set(id3, "sql", "SELECT * FROM albums LIMIT 5")

        # Verify all queries stored independently
        assert cache.size() == 3
        assert cache.get(id1, "question") == "How many customers?"
        assert cache.get(id2, "question") == "List all artists"
        assert cache.get(id3, "question") == "Top 5 albums"

        # Verify get_all works
        all_questions = cache.get_all("question")
        assert len(all_questions) == 3

    def test_cache_data_types(self):
        """Test storing different data types in cache."""
        cache = MemoryCache()
        cache_id = cache.generate_id()

        # String
        cache.set(cache_id, "string_field", "test string")
        assert cache.get(cache_id, "string_field") == "test string"

        # Integer
        cache.set(cache_id, "int_field", 42)
        assert cache.get(cache_id, "int_field") == 42

        # List
        cache.set(cache_id, "list_field", [1, 2, 3])
        assert cache.get(cache_id, "list_field") == [1, 2, 3]

        # Dict
        cache.set(cache_id, "dict_field", {"key": "value"})
        assert cache.get(cache_id, "dict_field") == {"key": "value"}

        # None
        cache.set(cache_id, "none_field", None)
        assert cache.get(cache_id, "none_field") is None

        # Boolean
        cache.set(cache_id, "bool_field", True)
        assert cache.get(cache_id, "bool_field") is True


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
