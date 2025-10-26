# TASK 02: Vanna Custom Class Implementation

**Status**: ⬜ Not Started
**Estimated Time**: 6-8 hours
**Dependencies**: TASK 01 (Claude Agent endpoint must be running)
**Phase**: 1 - Core Backend Setup

---

## OVERVIEW

Implement custom Vanna AI classes that integrate with Claude Agent SDK endpoint. Create `ClaudeAgentChat` class (LLM interface) and `DetomoVanna` class (combines ChromaDB + ClaudeAgentChat).

**Reference**: PRD Section 4.2.2

---

## OBJECTIVES

1. Create `src/detomo_vanna.py` module
2. Implement `ClaudeAgentChat` class (custom LLM class)
3. Implement `DetomoVanna` class (main Vanna class)
4. Test integration with Claude Agent SDK endpoint
5. Write unit tests

---

## DEPENDENCIES

### Python Packages

Add to `requirements.txt`:
```
vanna==0.7.9
chromadb<1.0.0
sentence-transformers>=2.2.0
requests>=2.31.0
```

Install:
```bash
uv pip install vanna chromadb sentence-transformers requests
```

### Prerequisites

- TASK 01 completed (Claude Agent endpoint running on http://localhost:8000)

---

## IMPLEMENTATION

### Step 1: Create Module Structure

```bash
mkdir -p src
touch src/__init__.py
```

### Step 2: Implement Custom Vanna Classes

Create `src/detomo_vanna.py`:

```python
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

        Returns:
            str: Generated SQL or text from Claude

        Raises:
            Exception: If API call fails
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
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize DetomoVanna.

        Args:
            config (dict): Configuration dictionary with keys:
                - path: ChromaDB storage path
                - client: ChromaDB client type ("persistent")
                - embedding_function: Embedding model name
                - agent_endpoint: Claude Agent SDK endpoint URL
                - model: Claude model name
                - temperature: LLM temperature
                - max_tokens: Max tokens for LLM
        """
        ChromaDB_VectorStore.__init__(self, config=config)
        ClaudeAgentChat.__init__(self, config=config)

        logger.info("Initialized DetomoVanna with ChromaDB + ClaudeAgentChat")
```

### Step 3: Create Basic Test Script

Create `test_detomo_vanna_basic.py` (for manual testing):

```python
"""Basic test script for DetomoVanna"""

from src.detomo_vanna import DetomoVanna
import os

def test_initialization():
    """Test DetomoVanna initialization"""
    print("Testing DetomoVanna initialization...")

    vn = DetomoVanna(config={
        # ChromaDB settings
        "path": "./test_vectordb",
        "client": "persistent",

        # Claude Agent SDK settings
        "agent_endpoint": "http://localhost:8000/generate",
        "model": "claude-sonnet-4-5",
        "temperature": 0.1,
        "max_tokens": 2048
    })

    print("✓ DetomoVanna initialized successfully")

    # Test submit_prompt
    print("\nTesting submit_prompt...")
    response = vn.submit_prompt("Generate SQL to count rows in Customer table")
    print(f"Response: {response}")

    print("\n✓ All tests passed!")

if __name__ == "__main__":
    # Make sure Claude Agent endpoint is running
    import requests
    try:
        r = requests.get("http://localhost:8000/health")
        if r.status_code == 200:
            test_initialization()
        else:
            print("ERROR: Claude Agent endpoint not healthy")
    except:
        print("ERROR: Claude Agent endpoint not running on http://localhost:8000")
        print("Please start it with: python claude_agent_server.py")
```

Run:
```bash
python test_detomo_vanna_basic.py
```

### Step 4: Write Unit Tests

Create `tests/unit/test_detomo_vanna.py`:

```python
import pytest
from unittest.mock import patch, MagicMock
from src.detomo_vanna import ClaudeAgentChat, DetomoVanna


class TestClaudeAgentChat:
    """Test ClaudeAgentChat class"""

    def test_initialization(self):
        """Test ClaudeAgentChat initialization with config"""
        config = {
            "agent_endpoint": "http://test:8000/generate",
            "model": "claude-sonnet-4-5",
            "temperature": 0.2,
            "max_tokens": 1024
        }

        chat = ClaudeAgentChat(config=config)

        assert chat.agent_endpoint == "http://test:8000/generate"
        assert chat.model == "claude-sonnet-4-5"
        assert chat.temperature == 0.2
        assert chat.max_tokens == 1024

    def test_message_formatting(self):
        """Test message formatting methods"""
        chat = ClaudeAgentChat(config={})

        assert chat.system_message("test") == {"role": "system", "content": "test"}
        assert chat.user_message("test") == {"role": "user", "content": "test"}
        assert chat.assistant_message("test") == {"role": "assistant", "content": "test"}

    @patch('src.detomo_vanna.requests.post')
    def test_submit_prompt_with_string(self, mock_post):
        """Test submit_prompt with string input"""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"text": "SELECT COUNT(*) FROM Customer"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        chat = ClaudeAgentChat(config={})
        result = chat.submit_prompt("Test prompt")

        assert result == "SELECT COUNT(*) FROM Customer"
        mock_post.assert_called_once()

    @patch('src.detomo_vanna.requests.post')
    def test_submit_prompt_with_messages(self, mock_post):
        """Test submit_prompt with list of messages"""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"text": "SELECT * FROM Customer"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        chat = ClaudeAgentChat(config={})
        messages = [
            {"role": "user", "content": "Show customers"}
        ]
        result = chat.submit_prompt(messages)

        assert result == "SELECT * FROM Customer"

    @patch('src.detomo_vanna.requests.post')
    def test_submit_prompt_timeout(self, mock_post):
        """Test submit_prompt handles timeout"""
        mock_post.side_effect = requests.exceptions.Timeout()

        chat = ClaudeAgentChat(config={})

        with pytest.raises(Exception, match="timeout"):
            chat.submit_prompt("Test prompt")

    @patch('src.detomo_vanna.requests.post')
    def test_submit_prompt_request_error(self, mock_post):
        """Test submit_prompt handles request errors"""
        mock_post.side_effect = requests.exceptions.RequestException("Network error")

        chat = ClaudeAgentChat(config={})

        with pytest.raises(Exception, match="Error calling Claude Agent SDK"):
            chat.submit_prompt("Test prompt")


class TestDetomoVanna:
    """Test DetomoVanna class"""

    @patch('src.detomo_vanna.ChromaDB_VectorStore.__init__')
    @patch('src.detomo_vanna.ClaudeAgentChat.__init__')
    def test_initialization(self, mock_claude_init, mock_chroma_init):
        """Test DetomoVanna initialization"""
        # Mock parent class __init__ methods
        mock_chroma_init.return_value = None
        mock_claude_init.return_value = None

        config = {
            "path": "./test_vectordb",
            "agent_endpoint": "http://localhost:8000/generate"
        }

        vn = DetomoVanna(config=config)

        # Verify both parent classes were initialized
        mock_chroma_init.assert_called_once_with(config=config)
        mock_claude_init.assert_called_once_with(config=config)
```

Run tests:
```bash
pytest tests/unit/test_detomo_vanna.py -v
```

---

## SUCCESS CRITERIA

- [ ] `src/detomo_vanna.py` created
- [ ] `ClaudeAgentChat` class implemented with all required methods
- [ ] `DetomoVanna` class implemented (inherits from ChromaDB + ClaudeAgentChat)
- [ ] Basic test script runs successfully
- [ ] Can initialize DetomoVanna with config
- [ ] Can call `submit_prompt()` successfully
- [ ] Unit tests created and passing (≥8 tests)
- [ ] Code coverage ≥80%

---

## TESTING CHECKLIST

### Manual Testing

1. Start Claude Agent endpoint:
   ```bash
   python claude_agent_server.py
   ```

2. Run basic test script:
   ```bash
   python test_detomo_vanna_basic.py
   ```

3. Verify ChromaDB folder created: `test_vectordb/`

### Unit Testing

```bash
pytest tests/unit/test_detomo_vanna.py -v --cov=src.detomo_vanna
```

---

## NEXT STEPS

After completing this task:

1. Update [TASK_MASTER.md](../TASK_MASTER.md) - mark TASK 02 as completed
2. Proceed to **TASK 03**: Training Data Preparation (can be done in parallel)
3. Or proceed to **TASK 04**: Training Script (requires TASK 03)

---

## REFERENCES

- **Vanna AI Docs**: https://vanna.ai/docs/
- **PRD Section 4.2.2**: Custom Vanna Class
- **PRD Section 4.2.1**: Vanna AI Framework

---

**Last Updated**: 2025-10-26
