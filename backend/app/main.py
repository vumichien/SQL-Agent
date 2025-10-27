"""
Main FastAPI application for Detomo SQL AI.

Initializes the application with all routers, middleware, and services.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .core.config import settings
from .routers import auth, query, training, health, llm
from .services.query_service import query_service
from .services.training_service import training_service
from .services.auto_train import auto_load_training_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Natural Language to SQL with Claude Agent SDK and Vanna AI"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory (legacy frontend in ../static)
try:
    app.mount("/static", StaticFiles(directory="../static"), name="static")
except RuntimeError:
    logger.warning("Static directory not found, skipping static file mounting")


# Include routers
# Health check (no prefix)
app.include_router(health.router)

# API v0 routes
app.include_router(auth.router, prefix=settings.API_V0_PREFIX)
app.include_router(query.router, prefix=settings.API_V0_PREFIX)
app.include_router(training.router, prefix=settings.API_V0_PREFIX)

# Internal LLM endpoint (used by Vanna)
app.include_router(llm.router)


@app.get("/")
async def root():
    """
    Serve the main UI (legacy frontend).

    Returns:
        FileResponse: index.html
    """
    try:
        return FileResponse("../static/index.html")
    except FileNotFoundError:
        return {
            "message": "Welcome to Detomo SQL AI",
            "version": settings.VERSION,
            "docs": "/docs",
            "health": "/api/v0/health"
        }


@app.on_event("startup")
async def startup_event():
    """
    Initialize services on application startup.

    - Initializes DetomoVanna with ChromaDB and SQLite
    - Sets up training service
    - Logs system information
    """
    logger.info("="*50)
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    logger.info("="*50)

    # Initialize Vanna
    try:
        logger.info("Initializing DetomoVanna...")
        query_service.initialize_vanna()

        # Set Vanna instance in training service
        training_service.set_vanna(query_service.vn)

        logger.info("✓ DetomoVanna initialized successfully")
        
        # Auto-load training data if empty
        logger.info("Checking training data...")
        auto_load_training_data(query_service.vn)
        
    except Exception as e:
        logger.error(f"✗ Failed to initialize DetomoVanna: {e}")
        raise

    logger.info("="*50)
    logger.info(f"Server ready at http://localhost:8000")
    logger.info(f"API docs at http://localhost:8000/docs")
    logger.info("="*50)


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Shutting down Detomo SQL AI...")

    # Shutdown thread pool executor
    if query_service.executor:
        query_service.executor.shutdown(wait=True)
        logger.info("Thread pool executor shut down")

    logger.info("Shutdown complete")
