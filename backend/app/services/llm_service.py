"""
LLM service for calling Claude Agent SDK.

Provides the internal /generate endpoint for Vanna.
"""

import logging
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock
from typing import Dict, Any

logger = logging.getLogger(__name__)


class LLMService:
    """Service for LLM generation using Claude Agent SDK."""

    @staticmethod
    async def call_claude_agent(
        prompt: str,
        model: str = "claude-sonnet-4-5",
        temperature: float = 0.1,
        max_tokens: int = 2048
    ) -> Dict[str, Any]:
        """
        Call Claude Agent SDK to generate SQL.

        Uses minimal configuration - no tools, no complex system prompt.
        Just basic LLM inference for Vanna.

        Args:
            prompt (str): The prompt to send to Claude
            model (str): Claude model to use
            temperature (float): Temperature for generation
            max_tokens (int): Maximum tokens to generate

        Returns:
            dict: Response with 'text' and 'model' keys

        Note:
            API key is automatically obtained from Claude Code environment.
            No need to set ANTHROPIC_API_KEY in .env file.

        Example:
            >>> result = await LLMService.call_claude_agent(
            ...     "Generate SQL for: How many customers?"
            ... )
            >>> print(result['text'])
            SELECT COUNT(*) FROM Customer
        """
        # Simple system prompt for SQL generation
        system_prompt = """You are a SQL expert. Generate accurate SQL queries based on the given context.

Rules:
- Generate ONLY the SQL query, no explanation
- Use proper SQL syntax
- Follow the database schema provided in the prompt
- Use similar examples as reference when provided"""

        # Configure Agent SDK with minimal options
        # Note: API key is automatically obtained from Claude Code environment
        options = ClaudeAgentOptions(
            system_prompt=system_prompt,
            model=model,
            max_turns=1,  # Single turn - just generate SQL
            permission_mode="bypassPermissions"  # No permission prompts needed
        )

        # Use Agent SDK (API key from Claude Code environment)
        async with ClaudeSDKClient(options=options) as client:
            # Send query to agent
            await client.query(prompt)

            # Collect response
            response_text = ""
            async for message in client.receive_response():
                # Check if it's an AssistantMessage
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        # Extract text from TextBlock
                        if isinstance(block, TextBlock):
                            response_text += block.text

            return {
                "text": response_text.strip(),
                "model": model
            }
