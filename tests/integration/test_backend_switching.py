"""
Test backend switching between Claude Agent SDK and Anthropic API

Run with: pytest tests/api/test_backend_switching.py -v
"""
import pytest
import sys
from pathlib import Path
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.llm.factory import create_llm_backend, get_available_backends
from backend.llm.claude_agent_backend import ClaudeAgentBackend
from backend.llm.anthropic_api_backend import AnthropicAPIBackend
from src.config import config


def test_get_available_backends():
    """Test getting list of available backends"""
    available = get_available_backends()
    assert isinstance(available, list)

    # If ANTHROPIC_API_KEY is set, we should have backends
    if os.getenv("ANTHROPIC_API_KEY"):
        assert len(available) > 0
        assert "claude_agent_sdk" in available or "anthropic_api" in available


@pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set"
)
def test_create_claude_agent_backend():
    """Test creating Claude Agent SDK backend"""
    backend = create_llm_backend(
        backend_type="claude_agent_sdk",
        config=config.get_llm_config()
    )

    assert backend is not None
    assert isinstance(backend, ClaudeAgentBackend)
    assert backend.get_backend_name() == "claude_agent_sdk"
    assert backend.is_available()


@pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set"
)
def test_create_anthropic_api_backend():
    """Test creating Anthropic API backend"""
    backend = create_llm_backend(
        backend_type="anthropic_api",
        config=config.get_llm_config()
    )

    assert backend is not None
    assert isinstance(backend, AnthropicAPIBackend)
    assert backend.get_backend_name() == "anthropic_api"
    assert backend.is_available()


def test_backend_without_api_key():
    """Test backend creation without API key"""
    # Temporarily remove API key
    original_key = os.getenv("ANTHROPIC_API_KEY")
    if original_key:
        os.environ.pop("ANTHROPIC_API_KEY", None)

    try:
        with pytest.raises(ValueError, match="No LLM backend available"):
            create_llm_backend(backend_type="claude_agent_sdk")
    finally:
        # Restore API key
        if original_key:
            os.environ["ANTHROPIC_API_KEY"] = original_key


@pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set"
)
def test_backend_submit_prompt():
    """Test submitting a prompt to both backends"""
    test_prompt = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say 'Hello World' in exactly two words."}
    ]

    # Test Claude Agent SDK backend
    backend1 = create_llm_backend(
        backend_type="claude_agent_sdk",
        config=config.get_llm_config()
    )
    response1 = backend1.submit_prompt(test_prompt)
    assert response1 is not None
    assert isinstance(response1, str)
    assert len(response1) > 0

    # Test Anthropic API backend
    backend2 = create_llm_backend(
        backend_type="anthropic_api",
        config=config.get_llm_config()
    )
    response2 = backend2.submit_prompt(test_prompt)
    assert response2 is not None
    assert isinstance(response2, str)
    assert len(response2) > 0


def test_backend_message_formatting():
    """Test message formatting methods"""
    backend = ClaudeAgentBackend()

    system_msg = backend.system_message("Test system")
    assert system_msg["role"] == "system"
    assert system_msg["content"] == "Test system"

    user_msg = backend.user_message("Test user")
    assert user_msg["role"] == "user"
    assert user_msg["content"] == "Test user"

    assistant_msg = backend.assistant_message("Test assistant")
    assert assistant_msg["role"] == "assistant"
    assert assistant_msg["content"] == "Test assistant"


def test_invalid_backend_type():
    """Test creating backend with invalid type"""
    with pytest.raises(ValueError, match="Unknown backend type"):
        create_llm_backend(backend_type="invalid_backend")


@pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set"
)
def test_backend_configuration():
    """Test backend configuration parameters"""
    custom_config = {
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.5,
        "max_tokens": 1024
    }

    backend = create_llm_backend(
        backend_type="claude_agent_sdk",
        config=custom_config
    )

    assert backend.model == "claude-3-5-sonnet-20241022"
    assert backend.temperature == 0.5
    assert backend.max_tokens == 1024
