"""
Health check and system status models.
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Basic health check response."""
    status: str
    service: str
    version: str


class APIHealthResponse(BaseModel):
    """Detailed API health check response."""
    status: str
    service: str
    version: str
    llm_endpoint: str
    database: str
    training_data_count: int
