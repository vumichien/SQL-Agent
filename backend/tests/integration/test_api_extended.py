"""
Integration Tests for Extended API Endpoints (TASK_07)

Tests for the 10 vanna-flask pattern endpoints added in TASK_07.

Author: Detomo SQL AI Team
Created: 2025-10-26
"""

import pytest
import requests
import json
import time

BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="module")
def ensure_server_running():
    """
    Ensure the server is running before tests.
    Waits up to 30 seconds for server to be healthy.
    """
    for i in range(30):
        try:
            response = requests.get(f"{BASE_URL}/api/v0/health", timeout=5)
            if response.status_code == 200:
                print("✓ Server is healthy")
                return
        except requests.exceptions.RequestException:
            if i < 29:
                time.sleep(1)
            else:
                pytest.fail("Server is not running. Please start claude_agent_server.py")


@pytest.fixture
def cache_id(ensure_server_running):
    """
    Generate a cached query by calling generate_sql endpoint.
    Returns the cache ID for use in other tests.
    """
    response = requests.post(
        f"{BASE_URL}/api/v0/generate_sql",
        json={"question": "How many customers are there?"}
    )
    assert response.status_code == 200
    data = response.json()
    return data["id"]


class TestGenerateQuestions:
    """Test /api/v0/generate_questions endpoint"""

    def test_generate_questions_success(self, ensure_server_running):
        """Test generating suggested questions"""
        response = requests.get(f"{BASE_URL}/api/v0/generate_questions")

        assert response.status_code == 200
        data = response.json()

        assert "questions" in data
        assert isinstance(data["questions"], list)
        assert len(data["questions"]) > 0

        print(f"✓ Generated {len(data['questions'])} questions")


class TestGenerateSQL:
    """Test /api/v0/generate_sql endpoint"""

    def test_generate_sql_success(self, ensure_server_running):
        """Test generating SQL from question"""
        response = requests.post(
            f"{BASE_URL}/api/v0/generate_sql",
            json={"question": "How many albums are there?"}
        )

        assert response.status_code == 200
        data = response.json()

        assert "id" in data
        assert "question" in data
        assert "sql" in data
        assert data["question"] == "How many albums are there?"
        assert "SELECT" in data["sql"].upper()
        assert "COUNT" in data["sql"].upper()

        print(f"✓ Generated SQL: {data['sql']}")

    def test_generate_sql_empty_question(self, ensure_server_running):
        """Test generating SQL with empty question"""
        response = requests.post(
            f"{BASE_URL}/api/v0/generate_sql",
            json={"question": ""}
        )

        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()


class TestRunSQL:
    """Test /api/v0/run_sql endpoint"""

    def test_run_sql_success(self, cache_id):
        """Test running SQL from cached query"""
        response = requests.post(
            f"{BASE_URL}/api/v0/run_sql",
            json={"id": cache_id}
        )

        assert response.status_code == 200
        data = response.json()

        assert "id" in data
        assert "results" in data
        assert "columns" in data
        assert "row_count" in data
        assert data["id"] == cache_id
        assert isinstance(data["results"], list)
        assert len(data["results"]) > 0
        assert data["row_count"] == len(data["results"])

        print(f"✓ Executed SQL - {data['row_count']} rows returned")

    def test_run_sql_invalid_id(self, ensure_server_running):
        """Test running SQL with invalid cache ID"""
        response = requests.post(
            f"{BASE_URL}/api/v0/run_sql",
            json={"id": "invalid-id-123"}
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestGeneratePlotlyFigure:
    """Test /api/v0/generate_plotly_figure endpoint"""

    def test_generate_plotly_figure_success(self, cache_id):
        """Test generating Plotly figure from cached query"""
        # First run the SQL to populate cache
        requests.post(f"{BASE_URL}/api/v0/run_sql", json={"id": cache_id})

        # Then generate figure
        response = requests.post(
            f"{BASE_URL}/api/v0/generate_plotly_figure",
            json={"id": cache_id}
        )

        assert response.status_code == 200
        data = response.json()

        assert "id" in data
        assert "figure" in data
        assert data["id"] == cache_id
        # Figure might be None for some queries (e.g., COUNT queries)

        print(f"✓ Generated Plotly figure (present: {data['figure'] is not None})")

    def test_generate_plotly_figure_without_run_sql(self, ensure_server_running):
        """Test generating figure without running SQL first"""
        # Generate SQL only, don't run it
        response1 = requests.post(
            f"{BASE_URL}/api/v0/generate_sql",
            json={"question": "How many tracks are there?"}
        )
        cache_id = response1.json()["id"]

        # Try to generate figure without running SQL
        response2 = requests.post(
            f"{BASE_URL}/api/v0/generate_plotly_figure",
            json={"id": cache_id}
        )

        assert response2.status_code == 400
        assert "missing" in response2.json()["detail"].lower()


class TestGenerateFollowupQuestions:
    """Test /api/v0/generate_followup_questions endpoint"""

    def test_generate_followup_questions_success(self, ensure_server_running):
        """Test generating followup questions"""
        response = requests.post(
            f"{BASE_URL}/api/v0/generate_followup_questions",
            json={
                "question": "How many customers are there?",
                "sql": "SELECT COUNT(*) FROM customers",
                "df": [{"COUNT(*)": 59}]
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert "questions" in data
        assert isinstance(data["questions"], list)
        # Followup questions might be empty, that's ok

        print(f"✓ Generated {len(data['questions'])} followup questions")

    def test_generate_followup_questions_minimal(self, ensure_server_running):
        """Test generating followup questions with minimal data"""
        response = requests.post(
            f"{BASE_URL}/api/v0/generate_followup_questions",
            json={"question": "Test question"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "questions" in data


class TestLoadQuestion:
    """Test /api/v0/load_question endpoint"""

    def test_load_question_success(self, cache_id):
        """Test loading complete cached query state"""
        # First run the SQL to populate cache
        requests.post(f"{BASE_URL}/api/v0/run_sql", json={"id": cache_id})

        # Load the cached state
        response = requests.post(
            f"{BASE_URL}/api/v0/load_question",
            json={"id": cache_id}
        )

        assert response.status_code == 200
        data = response.json()

        assert "id" in data
        assert "question" in data
        assert "sql" in data
        assert "results" in data
        assert "columns" in data
        assert "row_count" in data
        assert data["id"] == cache_id
        assert data["question"] == "How many customers are there?"
        assert data["results"] is not None
        assert len(data["results"]) > 0

        print(f"✓ Loaded cached query with {data['row_count']} results")

    def test_load_question_invalid_id(self, ensure_server_running):
        """Test loading question with invalid ID"""
        response = requests.post(
            f"{BASE_URL}/api/v0/load_question",
            json={"id": "invalid-id-456"}
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestGetQuestionHistory:
    """Test /api/v0/get_question_history endpoint"""

    def test_get_question_history_success(self, cache_id):
        """Test getting question history"""
        # Ensure at least one question in history (cache_id fixture)
        response = requests.get(f"{BASE_URL}/api/v0/get_question_history")

        assert response.status_code == 200
        data = response.json()

        assert "history" in data
        assert isinstance(data["history"], list)
        assert len(data["history"]) > 0

        # Check structure of history items
        first_item = data["history"][0]
        assert "id" in first_item
        assert "question" in first_item

        print(f"✓ Retrieved {len(data['history'])} questions from history")


class TestGetTrainingData:
    """Test /api/v0/get_training_data endpoint"""

    def test_get_training_data_success(self, ensure_server_running):
        """Test getting all training data"""
        response = requests.get(f"{BASE_URL}/api/v0/get_training_data")

        assert response.status_code == 200
        data = response.json()

        assert "training_data" in data
        assert "count" in data
        assert isinstance(data["training_data"], list)
        assert data["count"] == len(data["training_data"])
        assert data["count"] > 0  # Should have training data from TASK_04

        print(f"✓ Retrieved {data['count']} training items")


class TestRemoveTrainingData:
    """Test /api/v0/remove_training_data endpoint"""

    def test_remove_training_data_invalid_id(self, ensure_server_running):
        """Test removing training data with invalid ID"""
        response = requests.post(
            f"{BASE_URL}/api/v0/remove_training_data",
            json={"id": "nonexistent-training-id-999"}
        )

        # Vanna's remove_training_data silently succeeds even with invalid IDs
        # This is expected behavior - returns 200 with success message
        assert response.status_code == 200
        assert response.json()["status"] == "success"

        print("✓ Correctly handles invalid training data ID (silent success)")


class TestDownloadCSV:
    """Test /api/v0/download_csv endpoint"""

    def test_download_csv_success(self, cache_id):
        """Test downloading CSV from cached query"""
        # First run the SQL to populate cache
        requests.post(f"{BASE_URL}/api/v0/run_sql", json={"id": cache_id})

        # Download CSV
        response = requests.get(
            f"{BASE_URL}/api/v0/download_csv",
            params={"id": cache_id}
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        assert "Content-Disposition" in response.headers
        assert "attachment" in response.headers["Content-Disposition"]

        # Check CSV content
        csv_content = response.text
        assert len(csv_content) > 0
        assert "COUNT" in csv_content  # Header row

        print(f"✓ Downloaded CSV ({len(csv_content)} bytes)")

    def test_download_csv_invalid_id(self, ensure_server_running):
        """Test downloading CSV with invalid ID"""
        response = requests.get(
            f"{BASE_URL}/api/v0/download_csv",
            params={"id": "invalid-csv-id-789"}
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestMultiStepWorkflow:
    """Test complete multi-step workflow"""

    def test_complete_workflow(self, ensure_server_running):
        """Test the complete multi-step workflow: generate_sql -> run_sql -> generate_figure -> load_question"""

        # Step 1: Generate SQL
        response1 = requests.post(
            f"{BASE_URL}/api/v0/generate_sql",
            json={"question": "List the top 5 customers by spending"}
        )
        assert response1.status_code == 200
        cache_id = response1.json()["id"]
        print(f"✓ Step 1: Generated SQL with cache ID {cache_id}")

        # Step 2: Run SQL
        response2 = requests.post(
            f"{BASE_URL}/api/v0/run_sql",
            json={"id": cache_id}
        )
        assert response2.status_code == 200
        results = response2.json()["results"]
        print(f"✓ Step 2: Executed SQL - {len(results)} rows")

        # Step 3: Generate visualization (optional, might fail for some queries)
        response3 = requests.post(
            f"{BASE_URL}/api/v0/generate_plotly_figure",
            json={"id": cache_id}
        )
        assert response3.status_code == 200
        print(f"✓ Step 3: Generated visualization")

        # Step 4: Load complete state
        response4 = requests.post(
            f"{BASE_URL}/api/v0/load_question",
            json={"id": cache_id}
        )
        assert response4.status_code == 200
        loaded_data = response4.json()

        # Verify all data is present
        assert loaded_data["question"] == "List the top 5 customers by spending"
        assert loaded_data["sql"] is not None
        assert loaded_data["results"] is not None
        assert loaded_data["row_count"] == len(results)
        print(f"✓ Step 4: Loaded complete cached state")

        # Step 5: Download CSV
        response5 = requests.get(
            f"{BASE_URL}/api/v0/download_csv",
            params={"id": cache_id}
        )
        assert response5.status_code == 200
        assert len(response5.text) > 0
        print(f"✓ Step 5: Downloaded CSV")

        # Step 6: Check history
        response6 = requests.get(f"{BASE_URL}/api/v0/get_question_history")
        assert response6.status_code == 200
        history = response6.json()["history"]
        assert any(item["id"] == cache_id for item in history)
        print(f"✓ Step 6: Found query in history")

        print("✓ Complete workflow test passed!")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
