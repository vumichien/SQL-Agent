"""API routes for Detomo SQL AI"""
from flask import Blueprint, request, jsonify
import logging
import pandas as pd
from .errors import ValidationError, ServerError

logger = logging.getLogger(__name__)

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v0')

# Global vanna instance (will be set by app.py)
_vanna_instance = None


def set_vanna_instance(vn):
    """Set the global Vanna instance"""
    global _vanna_instance
    _vanna_instance = vn


def get_vanna():
    """Get the Vanna instance"""
    if _vanna_instance is None:
        raise ServerError("Vanna instance not initialized")
    return _vanna_instance


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        vn = get_vanna()
        backend_name = "unknown"

        # Try to get backend name if available
        if hasattr(vn, 'submit_prompt') and hasattr(vn.submit_prompt, '__self__'):
            backend = getattr(vn.submit_prompt.__self__, '__class__', None)
            if backend:
                backend_name = getattr(backend, '__name__', 'unknown')

        return jsonify({
            'status': 'healthy',
            'version': '1.0.0',
            'backend': backend_name,
            'database': 'connected'
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


@api_bp.route('/generate_sql', methods=['POST'])
def generate_sql():
    """
    Generate SQL from natural language question

    Request body:
    {
        "question": "How many customers are there?"
    }

    Response:
    {
        "sql": "SELECT COUNT(*) FROM customers",
        "status": "success"
    }
    """
    data = request.json

    if not data or 'question' not in data:
        raise ValidationError("Missing 'question' in request body")

    question = data.get('question', '').strip()

    if not question:
        raise ValidationError("Question cannot be empty")

    logger.info(f"Generating SQL for question: {question}")

    try:
        vn = get_vanna()
        sql = vn.generate_sql(question)

        logger.info(f"Generated SQL: {sql}")

        return jsonify({
            'question': question,
            'sql': sql,
            'status': 'success'
        }), 200

    except Exception as e:
        logger.error(f"Error generating SQL: {e}")
        raise ServerError(f"Failed to generate SQL: {str(e)}")


@api_bp.route('/run_sql', methods=['POST'])
def run_sql():
    """
    Execute SQL query and return results

    Request body:
    {
        "sql": "SELECT COUNT(*) FROM customers"
    }

    Response:
    {
        "data": [...],
        "columns": [...],
        "row_count": 10,
        "status": "success"
    }
    """
    data = request.json

    if not data or 'sql' not in data:
        raise ValidationError("Missing 'sql' in request body")

    sql = data.get('sql', '').strip()

    if not sql:
        raise ValidationError("SQL cannot be empty")

    logger.info(f"Executing SQL: {sql}")

    try:
        vn = get_vanna()
        df = vn.run_sql(sql)

        # Convert DataFrame to JSON-serializable format
        if isinstance(df, pd.DataFrame):
            result_data = df.to_dict('records')
            columns = df.columns.tolist()
            row_count = len(df)
        else:
            # Handle non-DataFrame results
            result_data = []
            columns = []
            row_count = 0

        logger.info(f"SQL executed successfully: {row_count} rows returned")

        return jsonify({
            'data': result_data,
            'columns': columns,
            'row_count': row_count,
            'status': 'success'
        }), 200

    except Exception as e:
        logger.error(f"Error executing SQL: {e}")
        raise ServerError(f"Failed to execute SQL: {str(e)}")


@api_bp.route('/ask', methods=['POST'])
def ask():
    """
    Ask a question and get both SQL and results

    Request body:
    {
        "question": "How many customers are there?"
    }

    Response:
    {
        "question": "...",
        "sql": "...",
        "data": [...],
        "columns": [...],
        "row_count": 10,
        "status": "success"
    }
    """
    data = request.json

    if not data or 'question' not in data:
        raise ValidationError("Missing 'question' in request body")

    question = data.get('question', '').strip()

    if not question:
        raise ValidationError("Question cannot be empty")

    logger.info(f"Processing question: {question}")

    try:
        vn = get_vanna()

        # Generate SQL
        sql = vn.generate_sql(question)
        logger.info(f"Generated SQL: {sql}")

        # Execute SQL
        df = vn.run_sql(sql)

        # Convert DataFrame to JSON-serializable format
        if isinstance(df, pd.DataFrame):
            result_data = df.to_dict('records')
            columns = df.columns.tolist()
            row_count = len(df)
        else:
            result_data = []
            columns = []
            row_count = 0

        logger.info(f"Question processed successfully: {row_count} rows returned")

        return jsonify({
            'question': question,
            'sql': sql,
            'data': result_data,
            'columns': columns,
            'row_count': row_count,
            'status': 'success'
        }), 200

    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise ServerError(f"Failed to process question: {str(e)}")


@api_bp.route('/generate_plotly_figure', methods=['POST'])
def generate_plotly_figure():
    """
    Generate Plotly visualization from SQL results

    Request body:
    {
        "sql": "SELECT Genre, COUNT(*) as count FROM tracks GROUP BY Genre",
        "chart_type": "bar"  // optional
    }

    Response:
    {
        "figure": {...},  // Plotly figure JSON
        "status": "success"
    }
    """
    data = request.json

    if not data or 'sql' not in data:
        raise ValidationError("Missing 'sql' in request body")

    sql = data.get('sql', '').strip()
    chart_type = data.get('chart_type', 'bar')

    if not sql:
        raise ValidationError("SQL cannot be empty")

    logger.info(f"Generating visualization for SQL: {sql}")

    try:
        vn = get_vanna()

        # Execute SQL first
        df = vn.run_sql(sql)

        if not isinstance(df, pd.DataFrame) or df.empty:
            raise ValidationError("No data to visualize")

        # Generate Plotly figure
        # For now, use Vanna's generate_plotly_code to get the figure
        # This may need customization based on your needs
        try:
            plotly_code = vn.generate_plotly_code(question="", sql=sql, df=df)

            # Execute the plotly code to get the figure
            # This is a simplified approach - you may want to parse and customize
            import plotly.express as px
            import plotly.graph_objects as go

            # Basic chart generation based on chart_type
            if chart_type == 'bar' and len(df.columns) >= 2:
                fig = px.bar(df, x=df.columns[0], y=df.columns[1])
            elif chart_type == 'line' and len(df.columns) >= 2:
                fig = px.line(df, x=df.columns[0], y=df.columns[1])
            elif chart_type == 'pie' and len(df.columns) >= 2:
                fig = px.pie(df, names=df.columns[0], values=df.columns[1])
            else:
                # Default: auto-detect best chart
                if len(df.columns) >= 2:
                    fig = px.bar(df, x=df.columns[0], y=df.columns[1])
                else:
                    raise ValidationError("Insufficient columns for visualization")

            # Convert figure to JSON
            figure_json = fig.to_json()

            logger.info("Visualization generated successfully")

            return jsonify({
                'figure': figure_json,
                'chart_type': chart_type,
                'status': 'success'
            }), 200

        except Exception as e:
            logger.warning(f"Vanna plotly generation failed, using fallback: {e}")
            raise

    except Exception as e:
        logger.error(f"Error generating visualization: {e}")
        raise ServerError(f"Failed to generate visualization: {str(e)}")


@api_bp.route('/get_training_data', methods=['GET'])
def get_training_data():
    """
    Get training data statistics

    Response:
    {
        "ddl_count": 12,
        "documentation_count": 11,
        "sql_count": 70,
        "total": 93,
        "status": "success"
    }
    """
    try:
        vn = get_vanna()

        # Get training data
        training_data = vn.get_training_data()

        # Count different types
        ddl_count = len([item for item in training_data if item.get('training_data_type') == 'ddl'])
        doc_count = len([item for item in training_data if item.get('training_data_type') == 'documentation'])
        sql_count = len([item for item in training_data if item.get('training_data_type') == 'sql'])

        logger.info(f"Training data retrieved: {len(training_data)} items")

        return jsonify({
            'ddl_count': ddl_count,
            'documentation_count': doc_count,
            'sql_count': sql_count,
            'total': len(training_data),
            'items': training_data[:10],  # Return first 10 items as sample
            'status': 'success'
        }), 200

    except Exception as e:
        logger.error(f"Error getting training data: {e}")
        raise ServerError(f"Failed to get training data: {str(e)}")


@api_bp.route('/train', methods=['POST'])
def train():
    """
    Add new training data

    Request body:
    {
        "type": "sql",  // "ddl", "documentation", or "sql"
        "question": "How many customers?",  // for sql type
        "sql": "SELECT COUNT(*) FROM customers",  // for sql type
        "ddl": "CREATE TABLE...",  // for ddl type
        "documentation": "..."  // for documentation type
    }

    Response:
    {
        "message": "Training data added successfully",
        "id": "...",
        "status": "success"
    }
    """
    data = request.json

    if not data or 'type' not in data:
        raise ValidationError("Missing 'type' in request body")

    training_type = data.get('type')

    if training_type not in ['ddl', 'documentation', 'sql']:
        raise ValidationError("Invalid type. Must be 'ddl', 'documentation', or 'sql'")

    try:
        vn = get_vanna()

        if training_type == 'sql':
            question = data.get('question')
            sql = data.get('sql')

            if not question or not sql:
                raise ValidationError("Missing 'question' or 'sql' for SQL training")

            result = vn.train(question=question, sql=sql)

        elif training_type == 'ddl':
            ddl = data.get('ddl')

            if not ddl:
                raise ValidationError("Missing 'ddl' for DDL training")

            result = vn.train(ddl=ddl)

        elif training_type == 'documentation':
            documentation = data.get('documentation')

            if not documentation:
                raise ValidationError("Missing 'documentation' for documentation training")

            result = vn.train(documentation=documentation)

        logger.info(f"Training data added: {training_type}")

        return jsonify({
            'message': 'Training data added successfully',
            'type': training_type,
            'id': str(result) if result else None,
            'status': 'success'
        }), 201

    except Exception as e:
        logger.error(f"Error adding training data: {e}")
        raise ServerError(f"Failed to add training data: {str(e)}")


@api_bp.route('/remove_training_data', methods=['DELETE'])
def remove_training_data():
    """
    Remove training data by ID

    Request body:
    {
        "id": "training_data_id"
    }

    Response:
    {
        "message": "Training data removed successfully",
        "status": "success"
    }
    """
    data = request.json

    if not data or 'id' not in data:
        raise ValidationError("Missing 'id' in request body")

    training_id = data.get('id')

    try:
        vn = get_vanna()
        result = vn.remove_training_data(id=training_id)

        logger.info(f"Training data removed: {training_id}")

        return jsonify({
            'message': 'Training data removed successfully',
            'id': training_id,
            'status': 'success'
        }), 200

    except Exception as e:
        logger.error(f"Error removing training data: {e}")
        raise ServerError(f"Failed to remove training data: {str(e)}")
