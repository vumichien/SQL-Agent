import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from claude_agent_server import app, call_claude_agent


@pytest.fixture
def client():
    """Create FastAPI test client"""
    return TestClient(app)


def test_health_endpoint(client):
    """Test /health endpoint returns correct status"""
    response = client.get('/health')
    data = response.json()

    assert response.status_code == 200
    assert data['status'] == 'healthy'
    assert data['service'] == 'Claude Agent SDK LLM Endpoint'
    assert data['version'] == '1.0.0'


@patch('claude_agent_server.call_claude_agent')
def test_generate_endpoint_success(mock_call_claude, client):
    """Test /generate endpoint with valid request"""
    # Mock the async function
    mock_call_claude.return_value = {
        "text": "SELECT COUNT(*) FROM Customer",
        "model": "claude-sonnet-4-5"
    }

    response = client.post(
        '/generate',
        json={
            "prompt": "How many customers?",
            "model": "claude-sonnet-4-5",
            "temperature": 0.1,
            "max_tokens": 2048
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert "text" in data
    assert data["text"] == "SELECT COUNT(*) FROM Customer"
    assert data["model"] == "claude-sonnet-4-5"
    mock_call_claude.assert_called_once()


def test_generate_endpoint_missing_prompt(client):
    """Test /generate endpoint with missing prompt"""
    response = client.post(
        '/generate',
        json={
            "model": "claude-sonnet-4-5"
        }
    )

    assert response.status_code == 422  # Validation error in FastAPI
    data = response.json()
    assert "detail" in data


@patch('claude_agent_server.call_claude_agent')
def test_generate_endpoint_error_handling(mock_call_claude, client):
    """Test /generate endpoint handles errors"""
    # Mock an error
    mock_call_claude.side_effect = Exception("API Error")

    response = client.post(
        '/generate',
        json={
            "prompt": "Test prompt",
            "model": "claude-sonnet-4-5"
        }
    )

    data = response.json()

    assert response.status_code == 500
    assert "detail" in data


def test_generate_endpoint_validation(client):
    """Test /generate endpoint input validation"""
    # Test temperature out of range
    response = client.post(
        '/generate',
        json={
            "prompt": "Test",
            "temperature": 1.5  # Invalid: > 1.0
        }
    )
    assert response.status_code == 422

    # Test max_tokens negative
    response = client.post(
        '/generate',
        json={
            "prompt": "Test",
            "max_tokens": -1  # Invalid: <= 0
        }
    )
    assert response.status_code == 422


@pytest.mark.asyncio
@patch('claude_agent_server.ClaudeSDKClient')
async def test_call_claude_agent(mock_client_class):
    """Test call_claude_agent function"""
    # Import the message types to properly check isinstance
    from claude_agent_sdk import AssistantMessage, TextBlock

    # Create mock TextBlock
    mock_text_block = MagicMock(spec=TextBlock)
    mock_text_block.text = "SELECT COUNT(*) FROM Customer"

    # Create mock AssistantMessage
    mock_message = MagicMock(spec=AssistantMessage)
    mock_message.content = [mock_text_block]

    # Create async generator function for receive_response
    async def mock_receive_response():
        yield mock_message

    # Create mock client
    mock_client = MagicMock()
    mock_client.query = AsyncMock()
    mock_client.receive_response = mock_receive_response

    # Mock the async context manager
    mock_client_class.return_value.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client_class.return_value.__aexit__ = AsyncMock()

    # Call the function
    result = await call_claude_agent(
        prompt="Test prompt",
        model="claude-sonnet-4-5",
        temperature=0.1,
        max_tokens=2048
    )

    assert result["text"] == "SELECT COUNT(*) FROM Customer"
    assert result["model"] == "claude-sonnet-4-5"
    mock_client.query.assert_called_once_with("Test prompt")
