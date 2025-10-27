"""
Query-related request and response models.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


# ============================================
# CORE QUERY MODELS
# ============================================

class QueryRequest(BaseModel):
    """Request for natural language query."""
    question: str = Field(..., description="Natural language question")
    language: Optional[str] = Field(default="en", description="Language: 'en' or 'jp'")


class QueryResponse(BaseModel):
    """Response for natural language query (all-in-one)."""
    id: str = Field(..., description="Cache ID for this query")
    question: str
    sql: str
    results: List[Dict[str, Any]]
    columns: List[str]
    visualization: Optional[Dict[str, Any]] = None
    row_count: int


# ============================================
# VANNA-FLASK PATTERN MODELS (Multi-step workflow)
# ============================================

class GenerateQuestionsResponse(BaseModel):
    """Response for suggested questions."""
    questions: List[str]


class GenerateSQLRequest(BaseModel):
    """Request to generate SQL from question."""
    question: str = Field(..., description="Natural language question")


class GenerateSQLResponse(BaseModel):
    """Response with generated SQL."""
    id: str = Field(..., description="Cache ID for this query")
    question: str
    sql: str


class RunSQLRequest(BaseModel):
    """Request to execute SQL."""
    id: str = Field(..., description="Cache ID from generate_sql")


class RunSQLResponse(BaseModel):
    """Response with SQL execution results."""
    id: str
    results: List[Dict[str, Any]]
    columns: List[str]
    row_count: int


class GeneratePlotlyFigureRequest(BaseModel):
    """Request to generate visualization."""
    id: str = Field(..., description="Cache ID from run_sql")


class GeneratePlotlyFigureResponse(BaseModel):
    """Response with Plotly figure."""
    id: str
    figure: Optional[Dict[str, Any]] = None


class GenerateFollowupQuestionsRequest(BaseModel):
    """Request to generate followup questions."""
    question: str = Field(..., description="Original question")
    sql: Optional[str] = None
    df: Optional[List[Dict[str, Any]]] = None


class GenerateFollowupQuestionsResponse(BaseModel):
    """Response with followup questions."""
    questions: List[str]


class LoadQuestionRequest(BaseModel):
    """Request to load cached question."""
    id: str = Field(..., description="Cache ID to load")


class LoadQuestionResponse(BaseModel):
    """Response with cached question data."""
    id: str
    question: Optional[str] = None
    sql: Optional[str] = None
    results: Optional[List[Dict[str, Any]]] = None
    columns: Optional[List[str]] = None
    figure: Optional[Dict[str, Any]] = None
    row_count: Optional[int] = None


class QuestionHistoryItem(BaseModel):
    """Single history item."""
    id: str
    question: str


class GetQuestionHistoryResponse(BaseModel):
    """Response with question history."""
    history: List[QuestionHistoryItem]
