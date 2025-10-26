"""Anthropic API backend implementation"""
import os
import logging
from typing import List, Dict, Any
from .base import LLMBackend

logger = logging.getLogger(__name__)


class AnthropicAPIBackend(LLMBackend):
    """
    Direct Anthropic API backend implementation.

    This backend uses the Anthropic API directly for simpler use cases
    or as a fallback when Claude Agent SDK is not needed.

    Advantages:
    - Simpler implementation
    - Lower latency (no SDK overhead)
    - More predictable behavior
    - Easier debugging
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize Anthropic API backend

        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self._client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the Anthropic API client"""
        try:
            import anthropic
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                self._client = anthropic.Anthropic(api_key=api_key)
                logger.info("Anthropic API backend initialized successfully")
            else:
                logger.warning("ANTHROPIC_API_KEY not found - backend unavailable")
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic API: {e}")
            self._client = None

    def submit_prompt(self, prompt: List[Dict[str, Any]], **kwargs) -> str:
        """
        Submit a prompt using Anthropic API

        Args:
            prompt: List of message dictionaries with 'role' and 'content'
            **kwargs: Additional arguments

        Returns:
            str: LLM response text

        Raises:
            ValueError: If backend is not available
        """
        if not self.is_available():
            raise ValueError("Anthropic API backend is not available. Check API key.")

        # Extract messages and system message
        messages = []
        system_message = ""

        for msg in prompt:
            role = msg.get("role")
            content = msg.get("content", "")

            if role == "system":
                system_message = content
            elif role in ["user", "assistant"]:
                messages.append({"role": role, "content": content})

        # Prepare system parameter
        system_param = system_message if system_message else None

        try:
            # Call Anthropic API
            response = self._client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_param,
                messages=messages
            )

            logger.debug(f"Anthropic API response received (usage: {response.usage})")
            return response.content[0].text

        except Exception as e:
            logger.error(f"Error in Anthropic API submit_prompt: {e}")
            raise

    def get_backend_name(self) -> str:
        """Get backend name"""
        return "anthropic_api"

    def is_available(self) -> bool:
        """Check if backend is available"""
        return self._client is not None
