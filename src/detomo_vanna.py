"""
Detomo Vanna - Custom Vanna AI implementation with Claude Agent SDK.

This module provides custom Vanna classes that integrate Claude Agent SDK
as the LLM backend instead of direct OpenAI/Anthropic API calls.
"""

from vanna.base import VannaBase
from vanna.chromadb import ChromaDB_VectorStore
import requests
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class ClaudeAgentChat(VannaBase):
    """
    Custom Vanna LLM class that calls Claude Agent SDK endpoint.

    This class implements Vanna's LLM interface to use Claude Agent SDK
    as the LLM backend instead of OpenAI/Anthropic API directly.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        VannaBase.__init__(self, config=config)

        # Claude Agent SDK endpoint
        self.agent_endpoint = config.get("agent_endpoint", "http://localhost:8000/generate")
        self.model = config.get("model", "claude-sonnet-4-5")
        self.temperature = config.get("temperature", 0.1)
        self.max_tokens = config.get("max_tokens", 2048)

        logger.info(f"Initialized ClaudeAgentChat with endpoint: {self.agent_endpoint}")

    def system_message(self, message: str) -> Dict[str, str]:
        """Format system message (Vanna interface)"""
        return {"role": "system", "content": message}

    def user_message(self, message: str) -> Dict[str, str]:
        """Format user message (Vanna interface)"""
        return {"role": "user", "content": message}

    def assistant_message(self, message: str) -> Dict[str, str]:
        """Format assistant message (Vanna interface)"""
        return {"role": "assistant", "content": message}

    def submit_prompt(self, prompt: Any, **kwargs) -> str:
        """
        Send prompt to Claude Agent SDK endpoint.

        This is the main method Vanna calls to get LLM responses.

        Args:
            prompt: List of message dicts or string
            **kwargs: Additional arguments (unused, for Vanna compatibility)

        Returns:
            str: Generated SQL or text from Claude

        Raises:
            Exception: If API call fails

        Example:
            >>> chat = ClaudeAgentChat(config={"agent_endpoint": "http://localhost:8000/generate"})
            >>> response = chat.submit_prompt("Generate SQL to count customers")
            >>> print(response)
            SELECT COUNT(*) FROM Customer
        """

        # Convert prompt to string if it's a list of messages
        if isinstance(prompt, list):
            # Extract just the content from messages
            prompt_text = "\n\n".join([
                f"{msg.get('role', 'user')}: {msg.get('content', '')}"
                for msg in prompt
            ])
        else:
            prompt_text = str(prompt)

        logger.info(f"Submitting prompt to {self.agent_endpoint} (length: {len(prompt_text)})")

        # Call Claude Agent SDK endpoint
        try:
            response = requests.post(
                self.agent_endpoint,
                json={
                    "prompt": prompt_text,
                    "model": self.model,
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens
                },
                timeout=30
            )
            response.raise_for_status()

            result = response.json()
            generated_text = result.get("text", "")

            logger.info(f"Received response (length: {len(generated_text)})")
            return generated_text

        except requests.exceptions.Timeout:
            logger.error(f"Timeout calling {self.agent_endpoint}")
            raise Exception(f"Claude Agent SDK timeout after 30s")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Claude Agent SDK: {str(e)}")
            raise Exception(f"Error calling Claude Agent SDK: {str(e)}")


class DetomoVanna(ChromaDB_VectorStore, ClaudeAgentChat):
    """
    Main Vanna class for Detomo SQL AI.

    Combines:
    - ChromaDB_VectorStore: For RAG retrieval
    - ClaudeAgentChat: For LLM generation via Claude Agent SDK

    Example:
        >>> vn = DetomoVanna(config={
        ...     "path": "./detomo_vectordb",
        ...     "agent_endpoint": "http://localhost:8000/generate",
        ...     "model": "claude-sonnet-4-5"
        ... })
        >>> vn.connect_to_sqlite("data/chinook.db")
        >>> sql = vn.generate_sql("How many customers are there?")
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize DetomoVanna.

        Args:
            config (dict): Configuration dictionary with keys:
                - path: ChromaDB storage path (default: "./detomo_vectordb")
                - client: ChromaDB client type (default: "persistent")
                - embedding_function: Embedding model name (optional)
                - agent_endpoint: Claude Agent SDK endpoint URL
                - model: Claude model name (default: "claude-sonnet-4-5")
                - temperature: LLM temperature (default: 0.1)
                - max_tokens: Max tokens for LLM (default: 2048)
        """
        ChromaDB_VectorStore.__init__(self, config=config)
        ClaudeAgentChat.__init__(self, config=config)

        logger.info("Initialized DetomoVanna with ChromaDB + ClaudeAgentChat")
