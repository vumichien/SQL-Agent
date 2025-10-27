"""
Query service for handling natural language to SQL queries.

Integrates with Vanna AI and manages query caching.
"""

import logging
import asyncio
import json
import numpy as np
from typing import Optional, List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from src.detomo_vanna import DetomoVanna
from src.cache import MemoryCache
from ..core.config import settings

logger = logging.getLogger(__name__)


def decode_plotly_bdata(obj):
    """
    Recursively decode Plotly's binary encoded data (bdata) back to lists.
    Plotly's to_plotly_json() encodes numpy arrays as bdata which causes
    issues in frontend rendering.
    """
    if isinstance(obj, dict):
        # Check if this is a bdata dict
        if 'bdata' in obj and 'dtype' in obj:
            # Decode the base64 encoded binary data
            import base64
            import struct
            
            dtype = obj['dtype']
            bdata = base64.b64decode(obj['bdata'])
            
            # Map dtype to struct format
            dtype_map = {
                'i1': 'b',  # int8
                'i2': 'h',  # int16
                'i4': 'i',  # int32
                'i8': 'q',  # int64
                'u1': 'B',  # uint8
                'u2': 'H',  # uint16
                'u4': 'I',  # uint32
                'u8': 'Q',  # uint64
                'f4': 'f',  # float32
                'f8': 'd',  # float64
            }
            
            fmt = dtype_map.get(dtype, 'd')
            count = len(bdata) // struct.calcsize(fmt)
            values = struct.unpack(f'{count}{fmt}', bdata)
            return list(values)
        else:
            # Recursively process dict
            return {key: decode_plotly_bdata(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [decode_plotly_bdata(item) for item in obj]
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    else:
        return obj


class QueryService:
    """Service for query generation and execution."""

    def __init__(self):
        """Initialize query service."""
        self.vn: Optional[DetomoVanna] = None
        self.cache = MemoryCache()
        self.executor = ThreadPoolExecutor(max_workers=4)

    def initialize_vanna(self):
        """
        Initialize DetomoVanna instance.

        Should be called on application startup.
        """
        try:
            logger.info("Initializing DetomoVanna...")

            self.vn = DetomoVanna(
                config={
                    "api_key": settings.ANTHROPIC_API_KEY,
                    "model": settings.CLAUDE_MODEL,
                    "path": settings.VECTOR_DB_PATH
                }
            )

            # Connect to database
            self.vn.connect_to_sqlite(settings.DATABASE_PATH)

            logger.info(f"DetomoVanna initialized successfully")
            logger.info(f"Vector DB: {settings.VECTOR_DB_PATH}")
            logger.info(f"Database: {settings.DATABASE_PATH}")

            # Log training data count
            training_data = self.vn.get_training_data()
            logger.info(f"Training data count: {len(training_data)}")

        except Exception as e:
            logger.error(f"Failed to initialize DetomoVanna: {e}")
            raise

    async def query(
        self,
        question: str,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        All-in-one query: Natural language → SQL → Results → Visualization.

        Args:
            question (str): Natural language question
            language (str): Language code ('en' or 'jp')

        Returns:
            dict: Query response with SQL, results, and visualization

        Raises:
            ValueError: If question is empty or Vanna not initialized

        Example:
            >>> service = QueryService()
            >>> result = await service.query("How many customers?")
            >>> print(result['sql'])
            SELECT COUNT(*) FROM Customer
        """
        if not self.vn:
            raise ValueError("DetomoVanna not initialized")

        if not question or len(question.strip()) == 0:
            raise ValueError("Missing or empty 'question' field")

        logger.info(f"Received query: {question}")

        # Run blocking Vanna calls in thread pool
        loop = asyncio.get_event_loop()

        # Generate SQL
        sql = await loop.run_in_executor(self.executor, self.vn.generate_sql, question)
        logger.info(f"Generated SQL: {sql}")

        # Execute SQL
        df = await loop.run_in_executor(self.executor, self.vn.run_sql, sql)

        # Generate visualization (optional)
        fig_json = None
        try:
            plotly_code = await loop.run_in_executor(
                self.executor,
                self.vn.generate_plotly_code,
                question,
                sql,
                df
            )
            fig = await loop.run_in_executor(self.executor, self.vn.get_plotly_figure, plotly_code, df)
            if fig:
                # Convert figure to dict, then recursively convert numpy arrays to lists
                # This prevents binary encoding (bdata) in the JSON response
                fig_dict = fig.to_plotly_json()
                fig_json = decode_plotly_bdata(fig_dict)
        except Exception as e:
            logger.warning(f"Could not generate visualization: {e}")

        # Convert DataFrame to dict
        results = df.to_dict(orient='records')
        columns = df.columns.tolist()

        # Generate cache ID for this query
        cache_id = self.cache.generate_id()
        self.cache.set(cache_id, "question", question)
        self.cache.set(cache_id, "sql", sql)
        self.cache.set(cache_id, "df", df)
        self.cache.set(cache_id, "results", results)
        self.cache.set(cache_id, "columns", columns)
        if fig_json:
            self.cache.set(cache_id, "figure", fig_json)

        logger.info(f"Query successful - {len(results)} rows returned")

        return {
            "id": cache_id,
            "question": question,
            "sql": sql,
            "results": results,
            "columns": columns,
            "visualization": fig_json,
            "row_count": len(results)
        }

    async def generate_questions(self) -> List[str]:
        """
        Generate suggested questions based on training data.

        Returns:
            list: List of suggested questions
        """
        if not self.vn:
            raise ValueError("DetomoVanna not initialized")

        loop = asyncio.get_event_loop()
        questions = await loop.run_in_executor(self.executor, self.vn.generate_questions)

        if not isinstance(questions, list):
            questions = []

        return questions

    async def generate_sql(self, question: str) -> Dict[str, Any]:
        """
        Generate SQL from question and cache the result.

        Args:
            question (str): Natural language question

        Returns:
            dict: Response with id, question, and sql
        """
        if not self.vn:
            raise ValueError("DetomoVanna not initialized")

        if not question or len(question.strip()) == 0:
            raise ValueError("Missing or empty 'question' field")

        loop = asyncio.get_event_loop()

        # Generate SQL
        sql = await loop.run_in_executor(self.executor, self.vn.generate_sql, question)

        # Cache the result
        cache_id = self.cache.generate_id()
        self.cache.set(cache_id, "question", question)
        self.cache.set(cache_id, "sql", sql)

        logger.info(f"Generated SQL cached with ID: {cache_id}")

        return {
            "id": cache_id,
            "question": question,
            "sql": sql
        }

    async def run_sql(self, cache_id: str) -> Dict[str, Any]:
        """
        Execute SQL from cached query.

        Args:
            cache_id (str): Cache ID from generate_sql

        Returns:
            dict: Response with id, results, columns, and row_count
        """
        if not self.vn:
            raise ValueError("DetomoVanna not initialized")

        if not self.cache.exists(cache_id):
            raise ValueError(f"Cache ID not found: {cache_id}")

        sql = self.cache.get(cache_id, "sql")
        if not sql:
            raise ValueError("No SQL found in cache for this ID")

        loop = asyncio.get_event_loop()

        # Execute SQL
        df = await loop.run_in_executor(self.executor, self.vn.run_sql, sql)

        # Cache results
        results = df.to_dict(orient='records')
        columns = df.columns.tolist()

        self.cache.set(cache_id, "df", df)
        self.cache.set(cache_id, "results", results)
        self.cache.set(cache_id, "columns", columns)

        logger.info(f"SQL executed - {len(results)} rows returned")

        return {
            "id": cache_id,
            "results": results,
            "columns": columns,
            "row_count": len(results)
        }

    async def generate_plotly_figure(self, cache_id: str) -> Dict[str, Any]:
        """
        Generate Plotly visualization from cached results.

        Args:
            cache_id (str): Cache ID from run_sql

        Returns:
            dict: Response with id and figure
        """
        if not self.vn:
            raise ValueError("DetomoVanna not initialized")

        if not self.cache.exists(cache_id):
            raise ValueError(f"Cache ID not found: {cache_id}")

        question = self.cache.get(cache_id, "question")
        sql = self.cache.get(cache_id, "sql")
        df = self.cache.get(cache_id, "df")

        if not all([question, sql, df is not None]):
            raise ValueError("Incomplete data in cache. Run generate_sql and run_sql first.")

        loop = asyncio.get_event_loop()

        fig_json = None
        try:
            plotly_code = await loop.run_in_executor(
                self.executor,
                self.vn.generate_plotly_code,
                question,
                sql,
                df
            )
            fig = await loop.run_in_executor(self.executor, self.vn.get_plotly_figure, plotly_code, df)
            if fig:
                # Convert figure to dict, then recursively convert numpy arrays to lists
                # This prevents binary encoding (bdata) in the JSON response
                fig_dict = fig.to_plotly_json()
                fig_json = decode_plotly_bdata(fig_dict)
                self.cache.set(cache_id, "figure", fig_json)
        except Exception as e:
            logger.warning(f"Could not generate visualization: {e}")

        return {
            "id": cache_id,
            "figure": fig_json
        }

    async def generate_followup_questions(
        self,
        question: str,
        sql: Optional[str] = None,
        df_data: Optional[List[Dict[str, Any]]] = None
    ) -> List[str]:
        """
        Generate followup questions.

        Args:
            question (str): Original question
            sql (str, optional): SQL query
            df_data (list, optional): DataFrame as list of dicts

        Returns:
            list: List of followup questions
        """
        if not self.vn:
            raise ValueError("DetomoVanna not initialized")

        loop = asyncio.get_event_loop()

        # Convert df_data back to DataFrame if provided
        import pandas as pd
        df = pd.DataFrame(df_data) if df_data else None

        questions = await loop.run_in_executor(
            self.executor,
            self.vn.generate_followup_questions,
            question,
            sql,
            df
        )

        if not isinstance(questions, list):
            questions = []

        return questions

    def load_question(self, cache_id: str) -> Dict[str, Any]:
        """
        Load cached question data.

        Args:
            cache_id (str): Cache ID

        Returns:
            dict: Cached data
        """
        if not self.cache.exists(cache_id):
            raise ValueError(f"Cache ID not found: {cache_id}")

        return {
            "id": cache_id,
            "question": self.cache.get(cache_id, "question"),
            "sql": self.cache.get(cache_id, "sql"),
            "results": self.cache.get(cache_id, "results"),
            "columns": self.cache.get(cache_id, "columns"),
            "figure": self.cache.get(cache_id, "figure"),
            "row_count": len(self.cache.get(cache_id, "results") or [])
        }

    def get_question_history(self) -> List[Dict[str, str]]:
        """
        Get all cached questions.

        Returns:
            list: List of question history items
        """
        all_questions = self.cache.get_all("question")
        history = []

        for item in all_questions:
            history.append({
                "id": item["id"],
                "question": item["question"]
            })

        return history

    async def download_csv(self, cache_id: str) -> str:
        """
        Generate CSV data from cached results.

        Args:
            cache_id (str): Cache ID

        Returns:
            str: CSV data

        Raises:
            ValueError: If cache ID not found or no results
        """
        if not self.cache.exists(cache_id):
            raise ValueError(f"Cache ID not found: {cache_id}")

        df = self.cache.get(cache_id, "df")
        if df is None:
            raise ValueError("No results found in cache for this ID")

        import io
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        return csv_buffer.getvalue()


# Global query service instance
query_service = QueryService()
