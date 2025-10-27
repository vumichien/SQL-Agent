"""
Training service for managing Vanna training data.

Handles adding, retrieving, and removing training data.
"""

import logging
from typing import Optional, List, Dict, Any
from src.detomo_vanna import DetomoVanna

logger = logging.getLogger(__name__)


class TrainingService:
    """Service for managing training data."""

    def __init__(self, vn: Optional[DetomoVanna] = None):
        """
        Initialize training service.

        Args:
            vn (DetomoVanna, optional): Vanna instance
        """
        self.vn = vn

    def set_vanna(self, vn: DetomoVanna):
        """Set Vanna instance."""
        self.vn = vn

    def add_training(
        self,
        ddl: Optional[str] = None,
        documentation: Optional[str] = None,
        question: Optional[str] = None,
        sql: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Add training data to Vanna.

        You can add:
        - DDL (CREATE TABLE statements)
        - Documentation (table/column descriptions)
        - Q&A pairs (question + SQL examples)

        Args:
            ddl (str, optional): DDL statement
            documentation (str, optional): Documentation text
            question (str, optional): Example question
            sql (str, optional): Example SQL query

        Returns:
            dict: Response with status and message

        Raises:
            ValueError: If Vanna not initialized or invalid data

        Examples:
            >>> service = TrainingService(vn)
            >>> service.add_training(ddl="CREATE TABLE customers (...)")
            {'status': 'success', 'message': 'DDL added to training data'}

            >>> service.add_training(
            ...     question="How many customers?",
            ...     sql="SELECT COUNT(*) FROM Customer"
            ... )
            {'status': 'success', 'message': 'Q&A pair added to training data'}
        """
        if not self.vn:
            raise ValueError("DetomoVanna not initialized")

        if ddl:
            self.vn.train(ddl=ddl)
            return {
                "status": "success",
                "message": "DDL added to training data"
            }

        elif documentation:
            self.vn.train(documentation=documentation)
            return {
                "status": "success",
                "message": "Documentation added to training data"
            }

        elif question and sql:
            self.vn.train(question=question, sql=sql)
            return {
                "status": "success",
                "message": "Q&A pair added to training data"
            }

        else:
            raise ValueError(
                "Invalid training data format. Provide 'ddl', 'documentation', or ('question' + 'sql')"
            )

    def get_training_data(self) -> Dict[str, Any]:
        """
        Get all training data.

        Returns:
            dict: Training data with count

        Raises:
            ValueError: If Vanna not initialized
        """
        if not self.vn:
            raise ValueError("DetomoVanna not initialized")

        training_data = self.vn.get_training_data()

        # Convert DataFrame to list of dicts if needed
        if hasattr(training_data, 'to_dict'):
            # It's a DataFrame
            training_data_list = training_data.to_dict(orient='records')
        elif isinstance(training_data, list):
            # It's already a list
            training_data_list = training_data
        else:
            training_data_list = []

        return {
            "training_data": training_data_list,
            "count": len(training_data_list)
        }

    def remove_training_data(self, training_id: str) -> Dict[str, str]:
        """
        Remove training data by ID.

        Args:
            training_id (str): Training data ID to remove

        Returns:
            dict: Response with status and message

        Raises:
            ValueError: If Vanna not initialized
        """
        if not self.vn:
            raise ValueError("DetomoVanna not initialized")

        try:
            self.vn.remove_training_data(id=training_id)
            return {
                "status": "success",
                "message": f"Training data {training_id} removed"
            }
        except Exception as e:
            logger.error(f"Error removing training data: {e}")
            raise ValueError(f"Failed to remove training data: {str(e)}")


# Global training service instance (will be initialized with vn on startup)
training_service = TrainingService()
