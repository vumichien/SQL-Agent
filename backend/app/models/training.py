"""
Training data management models.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class TrainRequest(BaseModel):
    """Request to add training data."""
    ddl: Optional[str] = Field(None, description="DDL statement")
    documentation: Optional[str] = Field(None, description="Table/column documentation")
    question: Optional[str] = Field(None, description="Example question")
    sql: Optional[str] = Field(None, description="Example SQL query")


class TrainResponse(BaseModel):
    """Response after adding training data."""
    status: str
    message: str


class GetTrainingDataResponse(BaseModel):
    """Response with all training data."""
    training_data: List[Dict[str, Any]]
    count: int


class RemoveTrainingDataRequest(BaseModel):
    """Request to remove training data."""
    id: str = Field(..., description="Training data ID to remove")


class RemoveTrainingDataResponse(BaseModel):
    """Response after removing training data."""
    status: str
    message: str
