"""
Integration tests for TASK_05: Core API Endpoints

Tests the FastAPI server with Vanna integration including:
- /api/v0/query endpoint (NL → SQL → Results)
- /api/v0/train endpoint (add training data)
- /api/v0/health endpoint (comprehensive health check)
- /generate endpoint (internal LLM endpoint)
- /health endpoint (internal health check)

Prerequisites:
- Server must be running on http://localhost:8000
- DetomoVanna must be initialized with training data
- Chinook database must be connected

Run with:
    pytest tests/integration/test_api_core.py -v
"""

import pytest
import requests
from time import sleep

BASE_URL = "http://localhost:8000"


def test_internal_health_endpoint():
    """Test internal LLM service health check"""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Claude Agent SDK LLM Endpoint"
    assert data["version"] == "1.0.0"


def test_api_health_endpoint():
    """Test comprehensive API health check"""
    response = requests.get(f"{BASE_URL}/api/v0/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Detomo SQL AI API"
    assert data["version"] == "2.0.0"
    assert data["llm_endpoint"] == "http://localhost:8000/generate"
    assert data["database"] == "data/chinook.db - Connected"
    assert data["training_data_count"] > 0


def test_query_endpoint_simple():
    """Test query endpoint with simple question"""
    response = requests.post(
        f"{BASE_URL}/api/v0/query",
        json={"question": "How many customers are there?"},
        timeout=60
    )
    assert response.status_code == 200
    data = response.json()

    # Check response structure
    assert "question" in data
    assert "sql" in data
    assert "results" in data
    assert "columns" in data
    assert "row_count" in data

    # Check SQL is generated
    assert len(data["sql"]) > 0
    assert "customers" in data["sql"].lower() or "customer" in data["sql"].lower()

    # Check results
    assert len(data["results"]) > 0
    assert data["row_count"] > 0


def test_query_endpoint_complex():
    """Test query endpoint with complex question"""
    response = requests.post(
        f"{BASE_URL}/api/v0/query",
        json={"question": "List the top 5 customers by total spending"},
        timeout=60
    )
    assert response.status_code == 200
    data = response.json()

    # Check response structure
    assert "sql" in data
    assert "results" in data

    # Check SQL contains expected keywords
    sql_lower = data["sql"].lower()
    assert "select" in sql_lower
    assert "limit 5" in sql_lower or "limit  5" in sql_lower

    # Check results
    assert len(data["results"]) <= 5
    assert data["row_count"] <= 5


def test_query_endpoint_japanese():
    """Test query endpoint with Japanese question"""
    response = requests.post(
        f"{BASE_URL}/api/v0/query",
        json={
            "question": "顧客は何人いますか？",
            "language": "jp"
        },
        timeout=60
    )
    assert response.status_code == 200
    data = response.json()

    # Check response
    assert "sql" in data
    assert "results" in data
    assert len(data["results"]) > 0


def test_query_endpoint_missing_question():
    """Test query endpoint with missing question"""
    response = requests.post(
        f"{BASE_URL}/api/v0/query",
        json={},
        timeout=10
    )
    assert response.status_code == 422  # Validation error


def test_query_endpoint_empty_question():
    """Test query endpoint with empty question"""
    response = requests.post(
        f"{BASE_URL}/api/v0/query",
        json={"question": ""},
        timeout=10
    )
    assert response.status_code == 400  # Bad request


def test_train_endpoint_qa_pair():
    """Test adding Q&A pair training data"""
    response = requests.post(
        f"{BASE_URL}/api/v0/train",
        json={
            "question": "How many test customers?",
            "sql": "SELECT COUNT(*) FROM customers WHERE FirstName = 'Test'"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "Q&A pair" in data["message"]


def test_train_endpoint_ddl():
    """Test adding DDL training data"""
    response = requests.post(
        f"{BASE_URL}/api/v0/train",
        json={
            "ddl": "CREATE TABLE test_table (id INTEGER PRIMARY KEY)"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "DDL" in data["message"]


def test_train_endpoint_documentation():
    """Test adding documentation training data"""
    response = requests.post(
        f"{BASE_URL}/api/v0/train",
        json={
            "documentation": "Test table stores test data"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "Documentation" in data["message"]


def test_train_endpoint_invalid():
    """Test train endpoint with invalid data"""
    response = requests.post(
        f"{BASE_URL}/api/v0/train",
        json={}
    )
    # Accept either 400 (bad request) or 500 (server error)
    assert response.status_code in [400, 500]


def test_internal_generate_endpoint():
    """Test internal /generate endpoint still works"""
    response = requests.post(
        f"{BASE_URL}/generate",
        json={
            "prompt": "Generate SQL to count customers",
            "model": "claude-sonnet-4-5"
        },
        timeout=30
    )
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "model" in data
    assert len(data["text"]) > 0


def test_internal_generate_endpoint_missing_prompt():
    """Test internal /generate endpoint with missing prompt"""
    response = requests.post(
        f"{BASE_URL}/generate",
        json={"model": "claude-sonnet-4-5"}
    )
    assert response.status_code == 422  # Validation error


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
