"""Error handling for Flask API"""
from flask import jsonify
import logging

logger = logging.getLogger(__name__)


class APIError(Exception):
    """Base API error"""
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        rv['status'] = 'error'
        return rv


class ValidationError(APIError):
    """Validation error (400)"""
    status_code = 400


class NotFoundError(APIError):
    """Not found error (404)"""
    status_code = 404


class ServerError(APIError):
    """Server error (500)"""
    status_code = 500


def register_error_handlers(app):
    """Register error handlers with Flask app"""

    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Handle API errors"""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        logger.error(f"API Error {error.status_code}: {error.message}")
        return response

    @app.errorhandler(404)
    def handle_404(error):
        """Handle 404 errors"""
        return jsonify({
            'error': 'Endpoint not found',
            'status': 'error'
        }), 404

    @app.errorhandler(500)
    def handle_500(error):
        """Handle 500 errors"""
        logger.error(f"Server error: {error}")
        return jsonify({
            'error': 'Internal server error',
            'status': 'error'
        }), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle unexpected exceptions"""
        logger.exception(f"Unexpected error: {error}")
        return jsonify({
            'error': 'An unexpected error occurred',
            'status': 'error',
            'details': str(error) if app.config.get('DEBUG') else None
        }), 500
