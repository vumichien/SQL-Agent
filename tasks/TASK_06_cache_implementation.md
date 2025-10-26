# TASK 06: Cache Implementation

**Status**: ⬜ Not Started
**Estimated Time**: 3-4 hours
**Dependencies**: None (can be done in parallel)
**Phase**: 3 - API Layer

---

## OVERVIEW

Implement in-memory cache for storing query state across API calls (vanna-flask pattern).

**Reference**: PRD Section 5.5

---

## IMPLEMENTATION

Create `cache.py`:

```python
import uuid


class MemoryCache:
    """In-memory cache for storing query state across API calls."""

    def __init__(self):
        self.cache = {}

    def generate_id(self) -> str:
        """Generate unique ID for cache entry"""
        return str(uuid.uuid4())

    def set(self, id: str, field: str, value):
        """Set a field for a specific ID"""
        if id not in self.cache:
            self.cache[id] = {}
        self.cache[id][field] = value

    def get(self, id: str, field: str):
        """Get a field for a specific ID"""
        if id not in self.cache:
            return None
        return self.cache[id].get(field)

    def get_all(self, field: str) -> list:
        """Get all values of a specific field across all cached entries."""
        result = []
        for cache_id, cache_data in self.cache.items():
            if field in cache_data:
                result.append({"id": cache_id, field: cache_data[field]})
        return result

    def delete(self, id: str):
        """Delete entire cache entry by ID"""
        if id in self.cache:
            del self.cache[id]
```

Create `tests/unit/test_cache.py`:

```python
import pytest
from cache import MemoryCache


def test_cache_set_and_get():
    cache = MemoryCache()
    cache_id = cache.generate_id()
    cache.set(cache_id, "question", "How many customers?")
    assert cache.get(cache_id, "question") == "How many customers?"


def test_cache_get_all():
    cache = MemoryCache()
    id1 = cache.generate_id()
    id2 = cache.generate_id()
    cache.set(id1, "question", "Q1")
    cache.set(id2, "question", "Q2")

    all_questions = cache.get_all("question")
    assert len(all_questions) == 2


def test_cache_delete():
    cache = MemoryCache()
    cache_id = cache.generate_id()
    cache.set(cache_id, "question", "Test")
    cache.delete(cache_id)
    assert cache.get(cache_id, "question") is None
```

---

## SUCCESS CRITERIA

- [ ] `cache.py` created
- [ ] All methods implemented
- [ ] Unit tests passing
- [ ] Coverage 100%

---

**Last Updated**: 2025-10-26
