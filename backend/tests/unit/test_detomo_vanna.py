"""Unit tests for DetomoVanna classes"""

import pytest
from unittest.mock import patch, MagicMock, Mock
import requests
from src.detomo_vanna import ClaudeAgentChat, DetomoVanna


class TestClaudeAgentChatViaDetomoVanna:
    """Test ClaudeAgentChat functionality through DetomoVanna"""

    @patch('src.detomo_vanna.ChromaDB_VectorStore.__init__', return_value=None)
    @patch('src.detomo_vanna.ClaudeAgentChat.__init__', return_value=None)
    def test_initialization_with_custom_config(self, mock_claude_init, mock_chroma_init):
        """Test initialization with custom config"""
        config = {
            "path": "./test_vectordb",
            "agent_endpoint": "http://test:8000/generate",
            "model": "claude-sonnet-4-5",
            "temperature": 0.2,
            "max_tokens": 1024
        }

        vn = DetomoVanna(config=config)

        # Manually set attributes since __init__ is mocked
        vn.agent_endpoint = config["agent_endpoint"]
        vn.model = config["model"]
        vn.temperature = config["temperature"]
        vn.max_tokens = config["max_tokens"]

        assert vn.agent_endpoint == "http://test:8000/generate"
        assert vn.model == "claude-sonnet-4-5"
        assert vn.temperature == 0.2
        assert vn.max_tokens == 1024

    @patch('src.detomo_vanna.ChromaDB_VectorStore.__init__', return_value=None)
    def test_system_message(self, mock_chroma_init):
        """Test system message formatting"""
        vn = DetomoVanna(config={})
        msg = vn.system_message("test system message")

        assert msg == {"role": "system", "content": "test system message"}
        assert msg["role"] == "system"
        assert msg["content"] == "test system message"

    @patch('src.detomo_vanna.ChromaDB_VectorStore.__init__', return_value=None)
    def test_user_message(self, mock_chroma_init):
        """Test user message formatting"""
        vn = DetomoVanna(config={})
        msg = vn.user_message("test user message")

        assert msg == {"role": "user", "content": "test user message"}
        assert msg["role"] == "user"
        assert msg["content"] == "test user message"

    @patch('src.detomo_vanna.ChromaDB_VectorStore.__init__', return_value=None)
    def test_assistant_message(self, mock_chroma_init):
        """Test assistant message formatting"""
        vn = DetomoVanna(config={})
        msg = vn.assistant_message("test assistant message")

        assert msg == {"role": "assistant", "content": "test assistant message"}
        assert msg["role"] == "assistant"
        assert msg["content"] == "test assistant message"

    @patch('src.detomo_vanna.ChromaDB_VectorStore.__init__', return_value=None)
    @patch('src.detomo_vanna.requests.post')
    def test_submit_prompt_with_string(self, mock_post, mock_chroma_init):
        """Test submit_prompt with string input"""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"text": "SELECT COUNT(*) FROM Customer"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        vn = DetomoVanna(config={})
        result = vn.submit_prompt("Test prompt")

        assert result == "SELECT COUNT(*) FROM Customer"
        mock_post.assert_called_once()

        # Verify the call arguments
        call_args = mock_post.call_args
        assert call_args[0][0] == "http://localhost:8000/generate"
        assert call_args[1]["json"]["prompt"] == "Test prompt"
        assert call_args[1]["json"]["model"] == "claude-sonnet-4-5"
        assert call_args[1]["timeout"] == 30

    @patch('src.detomo_vanna.ChromaDB_VectorStore.__init__', return_value=None)
    @patch('src.detomo_vanna.requests.post')
    def test_submit_prompt_with_messages(self, mock_post, mock_chroma_init):
        """Test submit_prompt with list of messages"""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"text": "SELECT * FROM Customer"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        vn = DetomoVanna(config={})
        messages = [
            {"role": "user", "content": "Show customers"}
        ]
        result = vn.submit_prompt(messages)

        assert result == "SELECT * FROM Customer"

        # Verify the prompt was formatted correctly
        call_args = mock_post.call_args
        assert "user: Show customers" in call_args[1]["json"]["prompt"]

    @patch('src.detomo_vanna.ChromaDB_VectorStore.__init__', return_value=None)
    @patch('src.detomo_vanna.requests.post')
    def test_submit_prompt_with_multiple_messages(self, mock_post, mock_chroma_init):
        """Test submit_prompt with multiple messages"""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"text": "SELECT * FROM Customer WHERE Country = 'USA'"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        vn = DetomoVanna(config={})
        messages = [
            {"role": "system", "content": "You are a SQL expert"},
            {"role": "user", "content": "Show US customers"}
        ]
        result = vn.submit_prompt(messages)

        assert result == "SELECT * FROM Customer WHERE Country = 'USA'"

        # Verify the prompt contains both messages
        call_args = mock_post.call_args
        prompt = call_args[1]["json"]["prompt"]
        assert "system: You are a SQL expert" in prompt
        assert "user: Show US customers" in prompt

    @patch('src.detomo_vanna.ChromaDB_VectorStore.__init__', return_value=None)
    @patch('src.detomo_vanna.requests.post')
    def test_submit_prompt_timeout(self, mock_post, mock_chroma_init):
        """Test submit_prompt handles timeout"""
        mock_post.side_effect = requests.exceptions.Timeout()

        vn = DetomoVanna(config={})

        with pytest.raises(Exception, match="timeout"):
            vn.submit_prompt("Test prompt")

    @patch('src.detomo_vanna.ChromaDB_VectorStore.__init__', return_value=None)
    @patch('src.detomo_vanna.requests.post')
    def test_submit_prompt_request_error(self, mock_post, mock_chroma_init):
        """Test submit_prompt handles request errors"""
        mock_post.side_effect = requests.exceptions.RequestException("Network error")

        vn = DetomoVanna(config={})

        with pytest.raises(Exception, match="Error calling Claude Agent SDK"):
            vn.submit_prompt("Test prompt")

    @patch('src.detomo_vanna.ChromaDB_VectorStore.__init__', return_value=None)
    @patch('src.detomo_vanna.requests.post')
    def test_submit_prompt_with_custom_temperature(self, mock_post, mock_chroma_init):
        """Test submit_prompt uses custom temperature"""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"text": "SQL response"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        vn = DetomoVanna(config={"temperature": 0.5})
        result = vn.submit_prompt("Test prompt")

        # Verify temperature was passed correctly
        call_args = mock_post.call_args
        assert call_args[1]["json"]["temperature"] == 0.5

    @patch('src.detomo_vanna.ChromaDB_VectorStore.__init__', return_value=None)
    @patch('src.detomo_vanna.requests.post')
    def test_submit_prompt_with_custom_max_tokens(self, mock_post, mock_chroma_init):
        """Test submit_prompt uses custom max_tokens"""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"text": "SQL response"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        vn = DetomoVanna(config={"max_tokens": 4096})
        result = vn.submit_prompt("Test prompt")

        # Verify max_tokens was passed correctly
        call_args = mock_post.call_args
        assert call_args[1]["json"]["max_tokens"] == 4096

    @patch('src.detomo_vanna.ChromaDB_VectorStore.__init__', return_value=None)
    @patch('src.detomo_vanna.requests.post')
    def test_submit_prompt_empty_response(self, mock_post, mock_chroma_init):
        """Test submit_prompt handles empty text in response"""
        # Mock response with empty text
        mock_response = MagicMock()
        mock_response.json.return_value = {"text": ""}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        vn = DetomoVanna(config={})
        result = vn.submit_prompt("Test prompt")

        assert result == ""


class TestDetomoVanna:
    """Test DetomoVanna class"""

    @patch('src.detomo_vanna.ChromaDB_VectorStore.__init__', return_value=None)
    @patch('src.detomo_vanna.ClaudeAgentChat.__init__', return_value=None)
    def test_initialization_calls_both_parents(self, mock_claude_init, mock_chroma_init):
        """Test DetomoVanna initialization calls both parent classes"""
        config = {
            "path": "./test_vectordb",
            "agent_endpoint": "http://localhost:8000/generate"
        }

        vn = DetomoVanna(config=config)

        # Verify both parent __init__ methods were called
        # They receive 'self' as first arg, hence we just check they were called
        assert mock_chroma_init.called
        assert mock_claude_init.called

    @patch('src.detomo_vanna.ChromaDB_VectorStore.__init__', return_value=None)
    @patch('src.detomo_vanna.ClaudeAgentChat.__init__', return_value=None)
    def test_initialization_with_empty_config(self, mock_claude_init, mock_chroma_init):
        """Test DetomoVanna initialization with empty config"""
        vn = DetomoVanna(config={})

        # Verify both parent classes were initialized
        assert mock_chroma_init.called
        assert mock_claude_init.called

    @patch('src.detomo_vanna.ChromaDB_VectorStore.__init__', return_value=None)
    @patch('src.detomo_vanna.ClaudeAgentChat.__init__', return_value=None)
    def test_initialization_with_none_config(self, mock_claude_init, mock_chroma_init):
        """Test DetomoVanna initialization with None config"""
        vn = DetomoVanna(config=None)

        # Verify both parent classes were initialized
        assert mock_chroma_init.called
        assert mock_claude_init.called
