from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock
import logging
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Claude Agent SDK LLM Endpoint")


# Request/Response models
class GenerateRequest(BaseModel):
    prompt: str
    model: str = "claude-haiku-4-5-20251001"
    temperature: float = 0.1
    max_tokens: int = 2048


class GenerateResponse(BaseModel):
    text: str
    model: str


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """
    LLM endpoint for Vanna using Claude Agent SDK.

    Receives prompt from Vanna, uses Claude Agent SDK, returns text.
    No database access, no tools, just simple LLM inference.
    """

    if not request.prompt:
        raise HTTPException(status_code=400, detail="Missing prompt")

    logger.info(f"Received request - Model: {request.model}, Prompt length: {len(request.prompt)}")

    try:
        result = await call_claude_agent(
            request.prompt,
            request.model,
            request.temperature,
            request.max_tokens
        )

        logger.info(f"Generated response - Length: {len(result['text'])}")
        return result

    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def call_claude_agent(prompt: str, model: str, temperature: float, max_tokens: int):
    """
    Call Claude Agent SDK to generate SQL.

    Uses minimal configuration - no tools, no complex system prompt.
    Just basic LLM inference for Vanna.

    Note: API key is automatically obtained from Claude Code environment.
    No need to set ANTHROPIC_API_KEY in .env file.
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


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Claude Agent SDK LLM Endpoint",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    logger.info("Starting Claude Agent SDK server on http://localhost:8000")
    logger.info("API key will be obtained automatically from Claude Code environment")
    uvicorn.run(
        app,
        port=8000,
        log_level="info"
    )
