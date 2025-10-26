"""Base LLM Backend interface"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class LLMBackend(ABC):
    """
    Abstract base class for LLM backends.

    This allows switching between different LLM implementations:
    - Claude Agent SDK (for advanced agent capabilities)
    - Anthropic API (direct API calls)
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the LLM backend

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.temperature = config.get("temperature", 0.1) if config else 0.1
        self.max_tokens = config.get("max_tokens", 2048) if config else 2048
        self.model = config.get("model", "claude-3-5-sonnet-20241022") if config else "claude-3-5-sonnet-20241022"

    @abstractmethod
    def submit_prompt(self, prompt: List[Dict[str, Any]], **kwargs) -> str:
        """
        Submit a prompt to the LLM and get a response

        Args:
            prompt: List of message dictionaries with 'role' and 'content'
            **kwargs: Additional arguments

        Returns:
            str: LLM response text
        """
        pass

    @abstractmethod
    def get_backend_name(self) -> str:
        """
        Get the name of the backend

        Returns:
            str: Backend name (e.g., "claude_agent_sdk", "anthropic_api")
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the backend is available and configured

        Returns:
            bool: True if backend is ready to use
        """
        pass

    def system_message(self, message: str) -> Dict[str, Any]:
        """Format system message"""
        return {"role": "system", "content": message}

    def user_message(self, message: str) -> Dict[str, Any]:
        """Format user message"""
        return {"role": "user", "content": message}

    def assistant_message(self, message: str) -> Dict[str, Any]:
        """Format assistant message"""
        return {"role": "assistant", "content": message}
