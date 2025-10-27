"""
LLM router for internal Vanna endpoint.

Provides the /generate endpoint used by Vanna's ClaudeAgentChat class.
"""

import logging
from fastapi import APIRouter, HTTPException
from ..models.llm import GenerateRequest, GenerateResponse
from ..services.llm_service import LLMService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["llm"])


@router.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """
    LLM endpoint for Vanna using Claude Agent SDK.

    Receives prompt from Vanna, uses Claude Agent SDK, returns text.
    No database access, no tools, just simple LLM inference.

    Args:
        request (GenerateRequest): LLM generation request

    Returns:
        GenerateResponse: Generated text from Claude

    Example:
        POST /generate
        {
            "prompt": "Generate SQL for: How many customers?",
            "model": "claude-sonnet-4-5",
            "temperature": 0.1,
            "max_tokens": 2048
        }

        Response:
        {
            "text": "SELECT COUNT(*) FROM Customer",
            "model": "claude-sonnet-4-5"
        }
    """
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Missing prompt")

    logger.info(f"Received request - Model: {request.model}, Prompt length: {len(request.prompt)}")

    try:
        result = await LLMService.call_claude_agent(
            request.prompt,
            request.model,
            request.temperature,
            request.max_tokens
        )

        logger.info(f"Generated response - Length: {len(result['text'])}")
        return GenerateResponse(**result)

    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
