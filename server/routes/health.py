from flask import Blueprint, Response
from utils.response_formatter import success_response
from typing import Tuple

# Create a Blueprint for health check route
health_bp = Blueprint('health', __name__)

@health_bp.route('/api/v1/health/status', methods=['GET'])
def health_check() -> Tuple[Response, int]:
    """
    Health check endpoint to verify API is running
    """
    return success_response(
        data={'status': 'healthy'},
        message="API is running"
    )
