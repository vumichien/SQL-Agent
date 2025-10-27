"""
Health check router.
"""

import logging
from fastapi import APIRouter, HTTPException
from ..models.health import HealthResponse, APIHealthResponse
from ..services.query_service import query_service
from ..core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health():
    """
    Basic health check endpoint.

    Returns:
        HealthResponse: Basic health status

    Example:
        GET /health

        Response:
        {
            "status": "healthy",
            "service": "Detomo SQL AI",
            "version": "3.0.0"
        }
    """
    return HealthResponse(
        status="healthy",
        service=settings.APP_NAME,
        version=settings.VERSION
    )


@router.get("/api/v0/health", response_model=APIHealthResponse)
async def api_health():
    """
    Comprehensive health check for the entire API.

    Checks:
    - Server status
    - DetomoVanna initialization
    - Database connection
    - Training data loaded
    - LLM endpoint available

    Returns:
        APIHealthResponse: Detailed health status

    Example:
        GET /api/v0/health

        Response:
        {
            "status": "healthy",
            "service": "Detomo SQL AI",
            "version": "3.0.0",
            "llm_endpoint": "http://localhost:8000/generate",
            "database": "data/chinook.db - Connected",
            "training_data_count": 93
        }
    """
    try:
        # Check Vanna initialized
        if not query_service.vn:
            raise HTTPException(status_code=503, detail="DetomoVanna not initialized")

        # Check training data
        training_data = query_service.vn.get_training_data()
        training_count = len(training_data)

        # Check database connection
        try:
            query_service.vn.run_sql("SELECT 1")
            db_status = f"{settings.DATABASE_PATH} - Connected"
        except Exception:
            db_status = f"{settings.DATABASE_PATH} - Disconnected"
            raise HTTPException(status_code=503, detail="Database not connected")

        return APIHealthResponse(
            status="healthy",
            service=settings.APP_NAME,
            version=settings.VERSION,
            llm_endpoint="http://localhost:8000/generate",
            database=db_status,
            training_data_count=training_count
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")
