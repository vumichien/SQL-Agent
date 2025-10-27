from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock
from src.detomo_vanna import DetomoVanna
from src.cache import MemoryCache
import logging
import uvicorn
from typing import Optional, Dict, Any, List
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
import io
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Claude Agent SDK LLM Endpoint",
    description="LLM endpoint for Vanna AI using Claude Agent SDK",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory (legacy frontend in root)
app.mount("/static", StaticFiles(directory="../static"), name="static")


# Request/Response models
class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="The prompt to send to Claude")
    model: str = Field(default="claude-sonnet-4-5", description="Claude model to use")
    temperature: float = Field(default=0.1, ge=0.0, le=1.0, description="Temperature for generation")
    max_tokens: int = Field(default=2048, gt=0, description="Maximum tokens to generate")


class GenerateResponse(BaseModel):
    text: str = Field(..., description="Generated text from Claude")
    model: str = Field(..., description="Model used for generation")


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


# ============================================
# PUBLIC API REQUEST/RESPONSE MODELS
# ============================================

class QueryRequest(BaseModel):
    question: str = Field(..., description="Natural language question")
    language: Optional[str] = Field(default="en", description="Language: 'en' or 'jp'")


class QueryResponse(BaseModel):
    question: str
    sql: str
    results: List[Dict[str, Any]]
    columns: List[str]
    visualization: Optional[Dict[str, Any]] = None
    row_count: int


class TrainRequest(BaseModel):
    ddl: Optional[str] = None
    documentation: Optional[str] = None
    question: Optional[str] = None
    sql: Optional[str] = None


class TrainResponse(BaseModel):
    status: str
    message: str


class APIHealthResponse(BaseModel):
    status: str
    service: str
    version: str
    llm_endpoint: str
    database: str
    training_data_count: int


# ============================================
# VANNA-FLASK PATTERN REQUEST/RESPONSE MODELS
# ============================================

class GenerateQuestionsResponse(BaseModel):
    questions: List[str]


class GenerateSQLRequest(BaseModel):
    question: str = Field(..., description="Natural language question")


class GenerateSQLResponse(BaseModel):
    id: str = Field(..., description="Cache ID for this query")
    question: str
    sql: str


class RunSQLRequest(BaseModel):
    id: str = Field(..., description="Cache ID from generate_sql")


class RunSQLResponse(BaseModel):
    id: str
    results: List[Dict[str, Any]]
    columns: List[str]
    row_count: int


class GeneratePlotlyFigureRequest(BaseModel):
    id: str = Field(..., description="Cache ID from run_sql")


class GeneratePlotlyFigureResponse(BaseModel):
    id: str
    figure: Optional[Dict[str, Any]] = None


class GenerateFollowupQuestionsRequest(BaseModel):
    question: str = Field(..., description="Original question")
    sql: Optional[str] = None
    df: Optional[List[Dict[str, Any]]] = None


class GenerateFollowupQuestionsResponse(BaseModel):
    questions: List[str]


class LoadQuestionRequest(BaseModel):
    id: str = Field(..., description="Cache ID to load")


class LoadQuestionResponse(BaseModel):
    id: str
    question: Optional[str] = None
    sql: Optional[str] = None
    results: Optional[List[Dict[str, Any]]] = None
    columns: Optional[List[str]] = None
    figure: Optional[Dict[str, Any]] = None
    row_count: Optional[int] = None


class QuestionHistoryItem(BaseModel):
    id: str
    question: str


class GetQuestionHistoryResponse(BaseModel):
    history: List[QuestionHistoryItem]


class GetTrainingDataResponse(BaseModel):
    training_data: List[Dict[str, Any]]
    count: int


class RemoveTrainingDataRequest(BaseModel):
    id: str = Field(..., description="Training data ID to remove")


# ============================================
# GLOBAL VARIABLES
# ============================================

# Global variable for Vanna instance
vn: Optional[DetomoVanna] = None

# Thread pool executor for running blocking Vanna calls
executor = ThreadPoolExecutor(max_workers=4)

# Initialize cache for multi-step workflows
cache = MemoryCache()


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
        return GenerateResponse(**result)

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
    return HealthResponse(
        status="healthy",
        service="Claude Agent SDK LLM Endpoint",
        version="1.0.0"
    )


@app.get("/")
async def root():
    """Serve the main UI (legacy frontend)"""
    return FileResponse("../static/index.html")


# ============================================
# PUBLIC API ENDPOINTS
# ============================================

@app.post("/api/v0/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    All-in-one endpoint: Natural language → SQL → Results → Visualization

    This is a simple endpoint for straightforward queries.
    For advanced workflows with caching, see TASK_07 endpoints.

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

    if not vn:
        raise HTTPException(status_code=500, detail="DetomoVanna not initialized")

    if not request.question or len(request.question.strip()) == 0:
        raise HTTPException(status_code=400, detail="Missing or empty 'question' field")

    logger.info(f"Received query: {request.question}")

    try:
        # Run blocking Vanna calls in thread pool to avoid deadlock
        loop = asyncio.get_event_loop()

        # Generate SQL (blocking call)
        sql = await loop.run_in_executor(executor, vn.generate_sql, request.question)
        logger.info(f"Generated SQL: {sql}")

        # Execute SQL (blocking call)
        df = await loop.run_in_executor(executor, vn.run_sql, sql)

        # Generate visualization (optional)
        fig_json = None
        try:
            # Generate plotly code
            plotly_code = await loop.run_in_executor(
                executor,
                vn.generate_plotly_code,
                request.question,
                sql,
                df
            )
            # Get figure
            fig = await loop.run_in_executor(executor, vn.get_plotly_figure, plotly_code)
            if fig:
                fig_json = json.loads(fig.to_json())
        except Exception as e:
            logger.warning(f"Could not generate visualization: {e}")

        # Convert DataFrame to dict
        results = df.to_dict(orient='records')
        columns = df.columns.tolist()

        logger.info(f"Query successful - {len(results)} rows returned")

        return QueryResponse(
            question=request.question,
            sql=sql,
            results=results,
            columns=columns,
            visualization=fig_json,
            row_count=len(results)
        )

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.post("/api/v0/train", response_model=TrainResponse)
async def train(request: TrainRequest):
    """
    Add training data to Vanna

    You can add:
    - DDL (CREATE TABLE statements)
    - Documentation (table/column descriptions)
    - Q&A pairs (question + SQL examples)

    Examples:
        # Add DDL
        POST /api/v0/train
        {"ddl": "CREATE TABLE customers (...)"}

        # Add documentation
        POST /api/v0/train
        {"documentation": "Customers table contains..."}

        # Add Q&A pair
        POST /api/v0/train
        {"question": "How many customers?", "sql": "SELECT COUNT(*) FROM Customer"}
    """

    if not vn:
        raise HTTPException(status_code=500, detail="DetomoVanna not initialized")

    try:
        if request.ddl:
            vn.train(ddl=request.ddl)
            return TrainResponse(status="success", message="DDL added to training data")

        elif request.documentation:
            vn.train(documentation=request.documentation)
            return TrainResponse(status="success", message="Documentation added to training data")

        elif request.question and request.sql:
            vn.train(question=request.question, sql=request.sql)
            return TrainResponse(status="success", message="Q&A pair added to training data")

        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid training data format. Provide 'ddl', 'documentation', or ('question' + 'sql')"
            )

    except Exception as e:
        logger.error(f"Error adding training data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")


@app.get("/api/v0/health", response_model=APIHealthResponse)
async def api_health():
    """
    Comprehensive health check for the entire API

    Checks:
    - Server status
    - DetomoVanna initialization
    - Database connection
    - Training data loaded
    - LLM endpoint available
    """

    try:
        # Check Vanna initialized
        if not vn:
            raise HTTPException(status_code=503, detail="DetomoVanna not initialized")

        # Check training data
        training_data = vn.get_training_data()
        training_count = len(training_data)

        # Check database connection
        try:
            vn.run_sql("SELECT 1")
            db_status = "data/chinook.db - Connected"
        except Exception:
            db_status = "data/chinook.db - Disconnected"
            raise HTTPException(status_code=503, detail="Database not connected")

        return APIHealthResponse(
            status="healthy",
            service="Detomo SQL AI API",
            version="2.0.0",
            llm_endpoint="http://localhost:8000/generate",
            database=db_status,
            training_data_count=training_count
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")


# ============================================
# VANNA-FLASK PATTERN ENDPOINTS (TASK_07)
# ============================================

@app.get("/api/v0/generate_questions", response_model=GenerateQuestionsResponse)
async def generate_questions():
    """
    Generate suggested questions based on training data.

    This endpoint helps users discover what questions they can ask.
    It generates sample questions based on the training data.

    Example:
        GET /api/v0/generate_questions

        Response:
        {
            "questions": [
                "How many customers are there?",
                "List the top 10 customers by spending",
                "What are the most popular genres?"
            ]
        }
    """

    if not vn:
        raise HTTPException(status_code=500, detail="DetomoVanna not initialized")

    try:
        loop = asyncio.get_event_loop()
        questions = await loop.run_in_executor(executor, vn.generate_questions)

        # Ensure we return a list
        if not isinstance(questions, list):
            questions = []

        return GenerateQuestionsResponse(questions=questions)

    except Exception as e:
        logger.error(f"Error generating questions: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate questions: {str(e)}")


@app.post("/api/v0/generate_sql", response_model=GenerateSQLResponse)
async def generate_sql(request: GenerateSQLRequest):
    """
    Generate SQL from natural language question and cache the result.

    This is the first step in the multi-step workflow.
    The generated SQL is cached with a unique ID.

    Example:
        POST /api/v0/generate_sql
        {"question": "How many customers are there?"}

        Response:
        {
            "id": "abc-123-def",
            "question": "How many customers are there?",
            "sql": "SELECT COUNT(*) FROM customers"
        }
    """

    if not vn:
        raise HTTPException(status_code=500, detail="DetomoVanna not initialized")

    if not request.question or len(request.question.strip()) == 0:
        raise HTTPException(status_code=400, detail="Missing or empty 'question' field")

    try:
        loop = asyncio.get_event_loop()

        # Generate SQL
        sql = await loop.run_in_executor(executor, vn.generate_sql, request.question)

        # Cache the result
        cache_id = cache.generate_id()
        cache.set(cache_id, "question", request.question)
        cache.set(cache_id, "sql", sql)

        logger.info(f"Generated SQL cached with ID: {cache_id}")

        return GenerateSQLResponse(
            id=cache_id,
            question=request.question,
            sql=sql
        )

    except Exception as e:
        logger.error(f"Error generating SQL: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate SQL: {str(e)}")


@app.post("/api/v0/run_sql", response_model=RunSQLResponse)
async def run_sql(request: RunSQLRequest):
    """
    Execute SQL from cached query.

    This is the second step in the multi-step workflow.
    Retrieves SQL from cache and executes it, then caches the results.

    Example:
        POST /api/v0/run_sql
        {"id": "abc-123-def"}

        Response:
        {
            "id": "abc-123-def",
            "results": [{"COUNT(*)": 59}],
            "columns": ["COUNT(*)"],
            "row_count": 1
        }
    """

    if not vn:
        raise HTTPException(status_code=500, detail="DetomoVanna not initialized")

    if not cache.exists(request.id):
        raise HTTPException(status_code=404, detail=f"Cache ID not found: {request.id}")

    sql = cache.get(request.id, "sql")
    if not sql:
        raise HTTPException(status_code=400, detail="No SQL found in cache for this ID")

    try:
        loop = asyncio.get_event_loop()

        # Execute SQL
        df = await loop.run_in_executor(executor, vn.run_sql, sql)

        # Cache the results
        cache.set(request.id, "df", df)

        # Convert to dict
        results = df.to_dict(orient='records')
        columns = df.columns.tolist()

        logger.info(f"SQL executed successfully - {len(results)} rows returned")

        return RunSQLResponse(
            id=request.id,
            results=results,
            columns=columns,
            row_count=len(results)
        )

    except Exception as e:
        logger.error(f"Error executing SQL: {e}")
        cache.set(request.id, "error", str(e))
        raise HTTPException(status_code=500, detail=f"Failed to execute SQL: {str(e)}")


@app.post("/api/v0/generate_plotly_figure", response_model=GeneratePlotlyFigureResponse)
async def generate_plotly_figure(request: GeneratePlotlyFigureRequest):
    """
    Generate Plotly visualization from cached query results.

    This is the third step in the multi-step workflow.
    Generates a visualization based on the question, SQL, and results.

    Example:
        POST /api/v0/generate_plotly_figure
        {"id": "abc-123-def"}

        Response:
        {
            "id": "abc-123-def",
            "figure": {...plotly JSON...}
        }
    """

    if not vn:
        raise HTTPException(status_code=500, detail="DetomoVanna not initialized")

    if not cache.exists(request.id):
        raise HTTPException(status_code=404, detail=f"Cache ID not found: {request.id}")

    question = cache.get(request.id, "question")
    sql = cache.get(request.id, "sql")
    df = cache.get(request.id, "df")

    if not question or not sql or df is None:
        raise HTTPException(
            status_code=400,
            detail="Missing cached data. Make sure to call generate_sql and run_sql first."
        )

    try:
        loop = asyncio.get_event_loop()

        # Generate plotly code
        plotly_code = await loop.run_in_executor(
            executor,
            vn.generate_plotly_code,
            question,
            sql,
            df
        )

        # Get figure
        fig = await loop.run_in_executor(executor, vn.get_plotly_figure, plotly_code)

        fig_json = None
        if fig:
            fig_json = json.loads(fig.to_json())
            cache.set(request.id, "fig", fig_json)

        logger.info(f"Plotly figure generated for cache ID: {request.id}")

        return GeneratePlotlyFigureResponse(
            id=request.id,
            figure=fig_json
        )

    except Exception as e:
        logger.warning(f"Could not generate visualization: {e}")
        # Don't raise an error - visualization is optional
        return GeneratePlotlyFigureResponse(
            id=request.id,
            figure=None
        )


@app.post("/api/v0/generate_followup_questions", response_model=GenerateFollowupQuestionsResponse)
async def generate_followup_questions(request: GenerateFollowupQuestionsRequest):
    """
    Generate follow-up questions based on the current query.

    Suggests related questions the user might want to ask next.

    Example:
        POST /api/v0/generate_followup_questions
        {
            "question": "How many customers are there?",
            "sql": "SELECT COUNT(*) FROM customers",
            "df": [{"COUNT(*)": 59}]
        }

        Response:
        {
            "questions": [
                "How many customers are from each country?",
                "What is the average customer spending?",
                "Who are the top 10 customers?"
            ]
        }
    """

    if not vn:
        raise HTTPException(status_code=500, detail="DetomoVanna not initialized")

    try:
        loop = asyncio.get_event_loop()

        # Convert df back to DataFrame if provided
        df = None
        if request.df:
            df = pd.DataFrame(request.df)

        # Generate followup questions
        questions = await loop.run_in_executor(
            executor,
            vn.generate_followup_questions,
            request.question,
            request.sql,
            df
        )

        # Ensure we return a list
        if not isinstance(questions, list):
            questions = []

        return GenerateFollowupQuestionsResponse(questions=questions)

    except Exception as e:
        logger.error(f"Error generating followup questions: {e}")
        # Return empty list instead of error
        return GenerateFollowupQuestionsResponse(questions=[])


@app.post("/api/v0/load_question", response_model=LoadQuestionResponse)
async def load_question(request: LoadQuestionRequest):
    """
    Load complete cached query state by ID.

    Retrieves all cached data for a specific query including question, SQL, results, and visualization.

    Example:
        POST /api/v0/load_question
        {"id": "abc-123-def"}

        Response:
        {
            "id": "abc-123-def",
            "question": "How many customers are there?",
            "sql": "SELECT COUNT(*) FROM customers",
            "results": [{"COUNT(*)": 59}],
            "columns": ["COUNT(*)"],
            "figure": {...},
            "row_count": 1
        }
    """

    if not cache.exists(request.id):
        raise HTTPException(status_code=404, detail=f"Cache ID not found: {request.id}")

    try:
        question = cache.get(request.id, "question")
        sql = cache.get(request.id, "sql")
        df = cache.get(request.id, "df")
        fig = cache.get(request.id, "fig")

        results = None
        columns = None
        row_count = None

        if df is not None:
            results = df.to_dict(orient='records')
            columns = df.columns.tolist()
            row_count = len(results)

        return LoadQuestionResponse(
            id=request.id,
            question=question,
            sql=sql,
            results=results,
            columns=columns,
            figure=fig,
            row_count=row_count
        )

    except Exception as e:
        logger.error(f"Error loading question: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load question: {str(e)}")


@app.get("/api/v0/get_question_history", response_model=GetQuestionHistoryResponse)
async def get_question_history():
    """
    Get history of all cached questions.

    Returns a list of all questions that have been asked and cached.

    Example:
        GET /api/v0/get_question_history

        Response:
        {
            "history": [
                {"id": "abc-123", "question": "How many customers?"},
                {"id": "def-456", "question": "Top 10 customers by spending"}
            ]
        }
    """

    try:
        all_questions = cache.get_all("question")

        history = [
            QuestionHistoryItem(id=item["id"], question=item["question"])
            for item in all_questions
        ]

        return GetQuestionHistoryResponse(history=history)

    except Exception as e:
        logger.error(f"Error getting question history: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get question history: {str(e)}")


@app.get("/api/v0/get_training_data")
async def get_training_data():
    """
    Get all training data.

    Returns all training examples (DDL, documentation, Q&A pairs) in ChromaDB.

    Example:
        GET /api/v0/get_training_data

        Response:
        {
            "training_data": [...],
            "count": 94
        }
    """

    if not vn:
        raise HTTPException(status_code=500, detail="DetomoVanna not initialized")

    try:
        training_data = vn.get_training_data()

        # Convert to JSON-serializable format
        # Vanna returns a DataFrame-like structure
        if hasattr(training_data, 'to_dict'):
            training_data = training_data.to_dict(orient='records')
        elif not isinstance(training_data, list):
            training_data = list(training_data) if training_data else []

        return {
            "training_data": training_data,
            "count": len(training_data)
        }

    except Exception as e:
        logger.error(f"Error getting training data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get training data: {str(e)}")


@app.post("/api/v0/remove_training_data")
async def remove_training_data(request: RemoveTrainingDataRequest):
    """
    Remove training data by ID.

    Deletes a specific training example from ChromaDB.

    Example:
        POST /api/v0/remove_training_data
        {"id": "abc-123-def"}

        Response:
        {"status": "success", "message": "Training data removed"}
    """

    if not vn:
        raise HTTPException(status_code=500, detail="DetomoVanna not initialized")

    try:
        vn.remove_training_data(id=request.id)

        return {"status": "success", "message": f"Training data removed: {request.id}"}

    except Exception as e:
        logger.error(f"Error removing training data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to remove training data: {str(e)}")


@app.get("/api/v0/download_csv")
async def download_csv(id: str = Query(..., description="Cache ID")):
    """
    Download query results as CSV file.

    Retrieves cached query results and returns them as a downloadable CSV file.

    Example:
        GET /api/v0/download_csv?id=abc-123-def

        Returns: CSV file download
    """

    if not cache.exists(id):
        raise HTTPException(status_code=404, detail=f"Cache ID not found: {id}")

    df = cache.get(id, "df")
    if df is None:
        raise HTTPException(status_code=400, detail="No results found in cache for this ID")

    try:
        # Convert DataFrame to CSV
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)

        # Get question for filename
        question = cache.get(id, "question")
        filename = "results.csv"
        if question:
            # Create safe filename from question
            safe_name = "".join(c for c in question if c.isalnum() or c in (' ', '-', '_'))[:50]
            filename = f"{safe_name}.csv"

        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        logger.error(f"Error downloading CSV: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to download CSV: {str(e)}")


@app.on_event("startup")
async def startup_event():
    """Initialize DetomoVanna and connect to database"""
    global vn

    logger.info("Claude Agent SDK server starting...")
    logger.info("Using Claude Code authentication")
    logger.info("Initializing DetomoVanna...")

    try:
        # Initialize Vanna
        vn = DetomoVanna(config={
            "path": "./detomo_vectordb",
            "client": "persistent",
            "agent_endpoint": "http://localhost:8000/generate",
            "model": "claude-sonnet-4-5"
        })

        # Connect to database
        vn.connect_to_sqlite("data/chinook.db")

        # Verify training data
        training_data = vn.get_training_data()
        logger.info(f"✓ DetomoVanna initialized with {len(training_data)} training items")
        logger.info("API documentation available at http://localhost:8000/docs")

    except Exception as e:
        logger.error(f"Failed to initialize DetomoVanna: {e}")
        raise


if __name__ == "__main__":
    logger.info("Starting Claude Agent SDK server on http://localhost:8000")
    logger.info("API key will be obtained automatically from Claude Code environment")
    uvicorn.run(
        app,
        port=8000,
        log_level="info"
    )
