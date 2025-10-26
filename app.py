"""
Detomo SQL AI - Flask Application

Main Flask application with support for:
- Claude Agent SDK backend (default)
- Anthropic API backend (fallback)
- Switchable backends via environment variable
"""
from flask import Flask, jsonify
from flask_cors import CORS
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import config
from api.routes import api_bp, set_vanna_instance
from api.errors import register_error_handlers
from backend.llm.factory import create_llm_backend, get_available_backends

# Import Vanna classes
from vanna.chromadb import ChromaDB_VectorStore


def create_detomo_vanna_with_backend(llm_backend):
    """
    Create a Vanna instance with the specified LLM backend

    Args:
        llm_backend: LLMBackend instance

    Returns:
        Vanna instance with the specified backend
    """

    class DetomoVanna(ChromaDB_VectorStore, llm_backend.__class__):
        """Detomo Vanna class with custom backend"""

        def __init__(self, config_dict=None, llm_backend_instance=None):
            # Initialize ChromaDB vector store
            ChromaDB_VectorStore.__init__(self, config=config_dict)

            # Copy LLM backend instance attributes
            if llm_backend_instance:
                self._client = llm_backend_instance._client
                self.temperature = llm_backend_instance.temperature
                self.max_tokens = llm_backend_instance.max_tokens
                self.model = llm_backend_instance.model

    # Create instance
    vanna_config = {
        "model": config.LLM_MODEL,
        "temperature": config.LLM_TEMPERATURE,
        "max_tokens": config.LLM_MAX_TOKENS,
        "path": config.VECTOR_DB_PATH,
    }

    vn = DetomoVanna(config_dict=vanna_config, llm_backend_instance=llm_backend)

    # Connect to database
    db_path = config.get_db_path()
    vn.connect_to_sqlite(db_path)

    return vn


def create_app():
    """Create and configure Flask application"""

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('detomo_sql_ai.log')
        ]
    )

    logger = logging.getLogger(__name__)

    # Create Flask app
    app = Flask(__name__)
    app.config.from_object(config)

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register error handlers
    register_error_handlers(app)

    # Initialize LLM backend
    logger.info("=" * 80)
    logger.info("DETOMO SQL AI - Starting Application")
    logger.info("=" * 80)

    # Check available backends
    available_backends = get_available_backends()
    logger.info(f"Available backends: {available_backends}")

    if not available_backends:
        logger.error("No LLM backends available! Please set ANTHROPIC_API_KEY.")
        logger.error("Application cannot start without an LLM backend.")
        sys.exit(1)

    # Create LLM backend
    try:
        backend_type = config.LLM_BACKEND
        logger.info(f"Attempting to create backend: {backend_type}")

        llm_backend = create_llm_backend(
            backend_type=backend_type,
            config=config.get_llm_config()
        )

        logger.info(f"✓ LLM Backend initialized: {llm_backend.get_backend_name()}")

    except Exception as e:
        logger.error(f"Failed to create LLM backend: {e}")
        logger.error("Application cannot start without an LLM backend.")
        sys.exit(1)

    # Create Vanna instance with backend
    try:
        logger.info("Initializing Vanna with LLM backend...")
        vn = create_detomo_vanna_with_backend(llm_backend)
        logger.info("✓ Vanna initialized successfully")

        # Set Vanna instance in routes
        set_vanna_instance(vn)

        # Get training stats
        try:
            training_data = vn.get_training_data()
            logger.info(f"✓ Training data loaded: {len(training_data)} items")
        except Exception as e:
            logger.warning(f"Could not load training data stats: {e}")

    except Exception as e:
        logger.error(f"Failed to initialize Vanna: {e}")
        logger.error("Application cannot start without Vanna.")
        sys.exit(1)

    # Register blueprints
    app.register_blueprint(api_bp)

    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'name': 'Detomo SQL AI',
            'version': '1.0.0',
            'backend': llm_backend.get_backend_name(),
            'status': 'running',
            'endpoints': {
                'health': '/api/v0/health',
                'generate_sql': '/api/v0/generate_sql',
                'run_sql': '/api/v0/run_sql',
                'ask': '/api/v0/ask',
                'generate_plotly_figure': '/api/v0/generate_plotly_figure',
                'get_training_data': '/api/v0/get_training_data',
                'train': '/api/v0/train',
                'remove_training_data': '/api/v0/remove_training_data',
            }
        })

    logger.info("=" * 80)
    logger.info("Application initialized successfully!")
    logger.info(f"Backend: {llm_backend.get_backend_name()}")
    logger.info(f"Database: {config.get_db_path()}")
    logger.info(f"Vector DB: {config.VECTOR_DB_PATH}")
    logger.info("=" * 80)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=config.DEBUG
    )
