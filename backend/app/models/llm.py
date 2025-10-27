"""
LLM endpoint models (internal /generate endpoint for Vanna).
"""

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    """Request for LLM generation (internal Vanna endpoint)."""
    prompt: str = Field(..., description="The prompt to send to Claude")
    model: str = Field(default="claude-sonnet-4-5", description="Claude model to use")
    temperature: float = Field(default=0.1, ge=0.0, le=1.0, description="Temperature for generation")
    max_tokens: int = Field(default=2048, gt=0, description="Maximum tokens to generate")


class GenerateResponse(BaseModel):
    """Response from LLM generation."""
    text: str = Field(..., description="Generated text from Claude")
    model: str = Field(..., description="Model used for generation")
