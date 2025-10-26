"""Factory for creating LLM backends"""
import os
import logging
from typing import Optional, Dict, Any
from .base import LLMBackend
from .claude_agent_backend import ClaudeAgentBackend
from .anthropic_api_backend import AnthropicAPIBackend

logger = logging.getLogger(__name__)


def create_llm_backend(
    backend_type: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None
) -> LLMBackend:
    """
    Factory function to create LLM backend

    Args:
        backend_type: Type of backend ('claude_agent_sdk', 'anthropic_api', or None for auto)
        config: Configuration dictionary

    Returns:
        LLMBackend: Initialized backend instance

    Raises:
        ValueError: If no backend is available
    """
    # Get backend type from environment if not specified
    if backend_type is None:
        backend_type = os.getenv("LLM_BACKEND", "claude_agent_sdk")

    logger.info(f"Creating LLM backend: {backend_type}")

    # Create backend based on type
    if backend_type == "claude_agent_sdk":
        backend = ClaudeAgentBackend(config)
        if backend.is_available():
            logger.info("Using Claude Agent SDK backend")
            return backend
        else:
            logger.warning("Claude Agent SDK not available, falling back to Anthropic API")
            backend = AnthropicAPIBackend(config)
            if backend.is_available():
                return backend

    elif backend_type == "anthropic_api":
        backend = AnthropicAPIBackend(config)
        if backend.is_available():
            logger.info("Using Anthropic API backend")
            return backend

    else:
        raise ValueError(f"Unknown backend type: {backend_type}")

    # If we get here, no backend is available
    raise ValueError(
        "No LLM backend available. Please set ANTHROPIC_API_KEY environment variable."
    )


def get_available_backends() -> list:
    """
    Get list of available backends

    Returns:
        list: List of available backend names
    """
    available = []

    # Check Claude Agent SDK
    try:
        backend = ClaudeAgentBackend()
        if backend.is_available():
            available.append("claude_agent_sdk")
    except Exception as e:
        logger.debug(f"Claude Agent SDK not available: {e}")

    # Check Anthropic API
    try:
        backend = AnthropicAPIBackend()
        if backend.is_available():
            available.append("anthropic_api")
    except Exception as e:
        logger.debug(f"Anthropic API not available: {e}")

    return available
