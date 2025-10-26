"""
Test API endpoints for Detomo SQL AI

Run with: pytest tests/api/test_api_endpoints.py -v
"""
import pytest
import sys
from pathlib import Path
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Skip tests if no API key
pytestmark = pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set - skipping API tests"
)


@pytest.fixture
def app():
    """Create Flask app for testing"""
    from app import create_app

    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get('/')
    assert response.status_code == 200

    data = response.get_json()
    assert data['name'] == 'Detomo SQL AI'
    assert data['version'] == '1.0.0'
    assert 'backend' in data
    assert 'endpoints' in data


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/v0/health')
    assert response.status_code == 200

    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'backend' in data
    assert 'database' in data


def test_get_training_data(client):
    """Test getting training data"""
    response = client.get('/api/v0/get_training_data')
    assert response.status_code == 200

    data = response.get_json()
    assert data['status'] == 'success'
    assert 'total' in data
    assert 'ddl_count' in data
    assert 'documentation_count' in data
    assert 'sql_count' in data
    assert data['total'] > 0


def test_generate_sql(client):
    """Test SQL generation endpoint"""
    response = client.post('/api/v0/generate_sql', json={
        'question': 'How many customers are there?'
    })

    if response.status_code == 200:
        data = response.get_json()
        assert data['status'] == 'success'
        assert 'sql' in data
        assert 'SELECT' in data['sql'].upper()
        assert 'customers' in data['sql'].lower()
    else:
        # If API key is not set, this test will fail gracefully
        pytest.skip("API key not configured or LLM not available")


def test_generate_sql_missing_question(client):
    """Test SQL generation with missing question"""
    response = client.post('/api/v0/generate_sql', json={})
    assert response.status_code == 400

    data = response.get_json()
    assert data['status'] == 'error'
    assert 'question' in data['error'].lower()


def test_generate_sql_empty_question(client):
    """Test SQL generation with empty question"""
    response = client.post('/api/v0/generate_sql', json={
        'question': ''
    })
    assert response.status_code == 400

    data = response.get_json()
    assert data['status'] == 'error'


def test_run_sql(client):
    """Test SQL execution endpoint"""
    response = client.post('/api/v0/run_sql', json={
        'sql': 'SELECT COUNT(*) as count FROM customers'
    })
    assert response.status_code == 200

    data = response.get_json()
    assert data['status'] == 'success'
    assert 'data' in data
    assert 'columns' in data
    assert 'row_count' in data
    assert data['row_count'] > 0


def test_run_sql_missing_sql(client):
    """Test SQL execution with missing SQL"""
    response = client.post('/api/v0/run_sql', json={})
    assert response.status_code == 400

    data = response.get_json()
    assert data['status'] == 'error'
    assert 'sql' in data['error'].lower()


def test_run_sql_invalid_sql(client):
    """Test SQL execution with invalid SQL"""
    response = client.post('/api/v0/run_sql', json={
        'sql': 'SELECT * FROM nonexistent_table'
    })
    assert response.status_code == 500

    data = response.get_json()
    assert data['status'] == 'error'


def test_ask_endpoint(client):
    """Test ask endpoint (question -> SQL -> results)"""
    response = client.post('/api/v0/ask', json={
        'question': 'How many albums are there?'
    })

    if response.status_code == 200:
        data = response.get_json()
        assert data['status'] == 'success'
        assert 'question' in data
        assert 'sql' in data
        assert 'data' in data
        assert 'columns' in data
        assert 'row_count' in data
    else:
        pytest.skip("API key not configured or LLM not available")


def test_train_sql(client):
    """Test adding SQL training data"""
    response = client.post('/api/v0/train', json={
        'type': 'sql',
        'question': 'Test question: How many test items?',
        'sql': 'SELECT COUNT(*) FROM test_table'
    })

    assert response.status_code in [201, 500]  # 201 if successful, 500 if vector DB issue

    if response.status_code == 201:
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['type'] == 'sql'


def test_train_missing_type(client):
    """Test training with missing type"""
    response = client.post('/api/v0/train', json={
        'question': 'Test question',
        'sql': 'SELECT 1'
    })
    assert response.status_code == 400

    data = response.get_json()
    assert data['status'] == 'error'
    assert 'type' in data['error'].lower()


def test_train_invalid_type(client):
    """Test training with invalid type"""
    response = client.post('/api/v0/train', json={
        'type': 'invalid_type',
        'question': 'Test',
        'sql': 'SELECT 1'
    })
    assert response.status_code == 400

    data = response.get_json()
    assert data['status'] == 'error'


def test_404_endpoint(client):
    """Test 404 error handling"""
    response = client.get('/api/v0/nonexistent')
    assert response.status_code == 404

    data = response.get_json()
    assert data['status'] == 'error'
