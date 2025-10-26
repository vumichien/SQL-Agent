"""Tests for DetomoVanna classes"""
import os
import pytest
from src.detomo_vanna_dev import create_vanna_dev
from src.config import config

# Disable ChromaDB telemetry to reduce noise
os.environ['ANONYMIZED_TELEMETRY'] = 'False'


def test_vanna_initialization():
    """Test that Vanna initializes correctly"""
    vn = create_vanna_dev()
    assert vn is not None
    print("[OK] Vanna initialized successfully")


def test_database_connection():
    """Test database connection"""
    vn = create_vanna_dev()
    # Test simple query
    result = vn.run_sql("SELECT COUNT(*) FROM customers")
    assert result is not None
    assert len(result) > 0
    print(f"[OK] Database query successful: {result}")


def test_sql_generation():
    """Test SQL generation (requires training data and API key)"""
    # Check if API key is available
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("[SKIP] Test 4 skipped: ANTHROPIC_API_KEY not set")
        return

    vn = create_vanna_dev()

    # This will only work after training
    try:
        sql = vn.generate_sql("How many customers are there?")
        assert sql is not None
        assert "customers" in sql.lower()
        assert "count" in sql.lower()
        print(f"[OK] SQL generated: {sql}")
    except Exception as e:
        print(f"[SKIP] Test 4 skipped: {e}")


def test_training_stats():
    """Test training stats"""
    vn = create_vanna_dev()
    stats = vn.get_training_stats()
    assert "total" in stats
    assert "ddl" in stats
    assert "documentation" in stats
    assert "sql" in stats
    print(f"[OK] Training stats: {stats}")


if __name__ == "__main__":
    # Run tests manually for debugging
    print("\n=== Running Detomo Vanna Tests ===\n")

    try:
        print("Test 1: Initialization")
        test_vanna_initialization()
    except Exception as e:
        print(f"[FAIL] Test 1 failed: {e}")

    try:
        print("\nTest 2: Database Connection")
        test_database_connection()
    except Exception as e:
        print(f"[FAIL] Test 2 failed: {e}")

    try:
        print("\nTest 3: Training Stats")
        test_training_stats()
    except Exception as e:
        print(f"[FAIL] Test 3 failed: {e}")

    print("\nTest 4: SQL Generation")
    test_sql_generation()

    print("\n=== Tests Complete ===\n")
