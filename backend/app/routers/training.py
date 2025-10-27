"""
Training router for managing Vanna training data.
"""

import logging
from fastapi import APIRouter, HTTPException
from ..models.training import (
    TrainRequest, TrainResponse,
    GetTrainingDataResponse,
    RemoveTrainingDataRequest, RemoveTrainingDataResponse
)
from ..services.training_service import training_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/training", tags=["training"])


@router.post("", response_model=TrainResponse)
async def train(request: TrainRequest):
    """
    Add training data to Vanna.

    You can add:
    - DDL (CREATE TABLE statements)
    - Documentation (table/column descriptions)
    - Q&A pairs (question + SQL examples)

    Args:
        request (TrainRequest): Training data to add

    Returns:
        TrainResponse: Status response

    Examples:
        # Add DDL
        POST /api/v0/training
        {"ddl": "CREATE TABLE customers (...)"}

        # Add documentation
        POST /api/v0/training
        {"documentation": "Customers table contains..."}

        # Add Q&A pair
        POST /api/v0/training
        {"question": "How many customers?", "sql": "SELECT COUNT(*) FROM Customer"}

        Response:
        {
            "status": "success",
            "message": "Q&A pair added to training data"
        }
    """
    try:
        result = training_service.add_training(
            ddl=request.ddl,
            documentation=request.documentation,
            question=request.question,
            sql=request.sql
        )
        return TrainResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error adding training data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")


@router.get("", response_model=GetTrainingDataResponse)
async def get_training_data():
    """
    Get all training data.

    Returns:
        GetTrainingDataResponse: All training data with count

    Example:
        GET /api/v0/training

        Response:
        {
            "training_data": [
                {"id": "1", "training_data_type": "sql", ...},
                {"id": "2", "training_data_type": "ddl", ...}
            ],
            "count": 93
        }
    """
    try:
        result = training_service.get_training_data()
        return GetTrainingDataResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting training data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get training data: {str(e)}")


@router.delete("/{id}", response_model=RemoveTrainingDataResponse)
async def remove_training_data(id: str):
    """
    Remove training data by ID.

    Args:
        id (str): Training data ID to remove

    Returns:
        RemoveTrainingDataResponse: Status response

    Example:
        DELETE /api/v0/training/abc-123

        Response:
        {
            "status": "success",
            "message": "Training data abc-123 removed"
        }
    """
    try:
        result = training_service.remove_training_data(id)
        return RemoveTrainingDataResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error removing training data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to remove training data: {str(e)}")
