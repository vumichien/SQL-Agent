"""
Query router for natural language to SQL operations.
"""

import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
import io

from ..models.query import (
    QueryRequest, QueryResponse,
    GenerateQuestionsResponse,
    GenerateSQLRequest, GenerateSQLResponse,
    RunSQLRequest, RunSQLResponse,
    GeneratePlotlyFigureRequest, GeneratePlotlyFigureResponse,
    GenerateFollowupQuestionsRequest, GenerateFollowupQuestionsResponse,
    LoadQuestionRequest, LoadQuestionResponse,
    GetQuestionHistoryResponse, QuestionHistoryItem
)
from ..services.query_service import query_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/query", tags=["query"])


# ============================================
# CORE QUERY ENDPOINT
# ============================================

@router.post("", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    All-in-one endpoint: Natural language → SQL → Results → Visualization.

    This is a simple endpoint for straightforward queries.
    For advanced workflows with caching, use the multi-step endpoints below.

    Args:
        request (QueryRequest): Query request with question

    Returns:
        QueryResponse: Complete query response

    Example:
        POST /api/v0/query
        {
            "question": "How many customers are there?",
            "language": "en"
        }

        Response:
        {
            "question": "How many customers are there?",
            "sql": "SELECT COUNT(*) FROM Customer",
            "results": [{"COUNT(*)": 59}],
            "columns": ["COUNT(*)"],
            "visualization": {...},
            "row_count": 1
        }
    """
    try:
        result = await query_service.query(request.question, request.language)
        return QueryResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


# ============================================
# MULTI-STEP WORKFLOW ENDPOINTS
# ============================================

@router.get("/generate_questions", response_model=GenerateQuestionsResponse)
async def generate_questions():
    """
    Generate suggested questions based on training data.

    Returns:
        GenerateQuestionsResponse: List of suggested questions

    Example:
        GET /api/v0/query/generate_questions

        Response:
        {
            "questions": [
                "How many customers are there?",
                "List the top 10 customers by spending",
                "What are the most popular genres?"
            ]
        }
    """
    try:
        questions = await query_service.generate_questions()
        return GenerateQuestionsResponse(questions=questions)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating questions: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate questions: {str(e)}")


@router.post("/generate_sql", response_model=GenerateSQLResponse)
async def generate_sql(request: GenerateSQLRequest):
    """
    Generate SQL from natural language question and cache the result.

    This is the first step in the multi-step workflow.

    Args:
        request (GenerateSQLRequest): Request with question

    Returns:
        GenerateSQLResponse: Generated SQL with cache ID

    Example:
        POST /api/v0/query/generate_sql
        {"question": "How many customers are there?"}

        Response:
        {
            "id": "abc-123-def",
            "question": "How many customers are there?",
            "sql": "SELECT COUNT(*) FROM Customer"
        }
    """
    try:
        result = await query_service.generate_sql(request.question)
        return GenerateSQLResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating SQL: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate SQL: {str(e)}")


@router.post("/run_sql", response_model=RunSQLResponse)
async def run_sql(request: RunSQLRequest):
    """
    Execute SQL from cached query.

    This is the second step in the multi-step workflow.

    Args:
        request (RunSQLRequest): Request with cache ID

    Returns:
        RunSQLResponse: SQL execution results

    Example:
        POST /api/v0/query/run_sql
        {"id": "abc-123-def"}

        Response:
        {
            "id": "abc-123-def",
            "results": [{"COUNT(*)": 59}],
            "columns": ["COUNT(*)"],
            "row_count": 1
        }
    """
    try:
        result = await query_service.run_sql(request.id)
        return RunSQLResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=404 if "not found" in str(e).lower() else 400, detail=str(e))
    except Exception as e:
        logger.error(f"Error running SQL: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to execute SQL: {str(e)}")


@router.post("/generate_plotly_figure", response_model=GeneratePlotlyFigureResponse)
async def generate_plotly_figure(request: GeneratePlotlyFigureRequest):
    """
    Generate Plotly visualization from cached results.

    This is the third step in the multi-step workflow.

    Args:
        request (GeneratePlotlyFigureRequest): Request with cache ID

    Returns:
        GeneratePlotlyFigureResponse: Plotly figure JSON

    Example:
        POST /api/v0/query/generate_plotly_figure
        {"id": "abc-123-def"}

        Response:
        {
            "id": "abc-123-def",
            "figure": {...}  // Plotly JSON
        }
    """
    try:
        result = await query_service.generate_plotly_figure(request.id)
        return GeneratePlotlyFigureResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=404 if "not found" in str(e).lower() else 400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating visualization: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate visualization: {str(e)}")


@router.post("/generate_followup_questions", response_model=GenerateFollowupQuestionsResponse)
async def generate_followup_questions(request: GenerateFollowupQuestionsRequest):
    """
    Generate followup questions based on results.

    Args:
        request (GenerateFollowupQuestionsRequest): Request with question, sql, and results

    Returns:
        GenerateFollowupQuestionsResponse: List of followup questions

    Example:
        POST /api/v0/query/generate_followup_questions
        {
            "question": "How many customers are there?",
            "sql": "SELECT COUNT(*) FROM Customer",
            "df": [{"COUNT(*)": 59}]
        }

        Response:
        {
            "questions": [
                "Who are the top 10 customers?",
                "What countries do customers live in?"
            ]
        }
    """
    try:
        questions = await query_service.generate_followup_questions(
            request.question,
            request.sql,
            request.df
        )
        return GenerateFollowupQuestionsResponse(questions=questions)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating followup questions: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate followup questions: {str(e)}")


@router.post("/load_question", response_model=LoadQuestionResponse)
async def load_question(request: LoadQuestionRequest):
    """
    Load cached question data.

    Args:
        request (LoadQuestionRequest): Request with cache ID

    Returns:
        LoadQuestionResponse: Cached question data

    Example:
        POST /api/v0/query/load_question
        {"id": "abc-123-def"}

        Response:
        {
            "id": "abc-123-def",
            "question": "How many customers are there?",
            "sql": "SELECT COUNT(*) FROM Customer",
            "results": [{"COUNT(*)": 59}],
            "columns": ["COUNT(*)"],
            "figure": {...},
            "row_count": 1
        }
    """
    try:
        result = query_service.load_question(request.id)
        return LoadQuestionResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error loading question: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load question: {str(e)}")


@router.get("/get_question_history", response_model=GetQuestionHistoryResponse)
async def get_question_history():
    """
    Get all cached questions (history).

    Returns:
        GetQuestionHistoryResponse: List of question history items

    Example:
        GET /api/v0/query/get_question_history

        Response:
        {
            "history": [
                {"id": "abc-123", "question": "How many customers?"},
                {"id": "def-456", "question": "Top 10 albums?"}
            ]
        }
    """
    try:
        history = query_service.get_question_history()
        history_items = [QuestionHistoryItem(**item) for item in history]
        return GetQuestionHistoryResponse(history=history_items)
    except Exception as e:
        logger.error(f"Error getting question history: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get question history: {str(e)}")


@router.get("/download_csv/{id}")
async def download_csv(id: str):
    """
    Download query results as CSV.

    Args:
        id (str): Cache ID

    Returns:
        StreamingResponse: CSV file download

    Example:
        GET /api/v0/query/download_csv/abc-123-def

        Response:
        (CSV file download)
    """
    try:
        csv_data = await query_service.download_csv(id)

        # Create CSV response
        csv_buffer = io.StringIO(csv_data)

        return StreamingResponse(
            iter([csv_data]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=query_{id}.csv"
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error downloading CSV: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to download CSV: {str(e)}")
