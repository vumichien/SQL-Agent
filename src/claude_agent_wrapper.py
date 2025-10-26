"""Claude Agent SDK wrapper for Vanna"""
import os
from typing import List, Dict, Any
from vanna.base import VannaBase


class ClaudeAgentChat(VannaBase):
    """
    Custom wrapper for Claude Agent SDK.
    This integrates the Agent SDK with Vanna framework.

    For development, uses Anthropic API directly.
    Can be extended to use Claude Agent SDK features in the future.
    """

    def __init__(self, config=None):
        VannaBase.__init__(self, config=config)

        # Config
        self.temperature = config.get("temperature", 0.1) if config else 0.1
        self.max_tokens = config.get("max_tokens", 2048) if config else 2048
        self.model = config.get("model", "claude-3-5-sonnet-20241022") if config else "claude-3-5-sonnet-20241022"

    def system_message(self, message: str) -> Dict[str, Any]:
        """Format system message"""
        return {"role": "system", "content": message}

    def user_message(self, message: str) -> Dict[str, Any]:
        """Format user message"""
        return {"role": "user", "content": message}

    def assistant_message(self, message: str) -> Dict[str, Any]:
        """Format assistant message"""
        return {"role": "assistant", "content": message}

    def submit_prompt(self, prompt: List[Dict[str, Any]], **kwargs) -> str:
        """
        Vanna calls this method to submit prompts to the LLM.
        We convert to Anthropic API format.

        Args:
            prompt: List of message dictionaries with 'role' and 'content'
            **kwargs: Additional arguments

        Returns:
            str: LLM response text
        """
        import anthropic

        # Get API key
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")

        client = anthropic.Anthropic(api_key=api_key)

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

        # Call Anthropic API
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=system_param,
            messages=messages
        )

        return response.content[0].text
