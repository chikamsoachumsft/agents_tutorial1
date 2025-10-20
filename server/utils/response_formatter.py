from flask import jsonify, Response
from datetime import datetime, timezone
from typing import Any, Optional

def format_response(
    success: bool = True,
    data: Any = None,
    message: str = "",
    status_code: int = 200
) -> tuple[Response, int]:
    """
    Format API response according to standard format
    
    Args:
        success: Whether the operation was successful
        data: Response data (object or array)
        message: Response message
        status_code: HTTP status code
    
    Returns:
        Tuple of (Response, status_code)
    """
    response_data = {
        "success": success,
        "data": data,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    }
    
    return jsonify(response_data), status_code

def success_response(data: Any = None, message: str = "Success", status_code: int = 200) -> tuple[Response, int]:
    """Return a successful response"""
    return format_response(success=True, data=data, message=message, status_code=status_code)

def error_response(message: str = "Error", status_code: int = 400, data: Any = None) -> tuple[Response, int]:
    """Return an error response"""
    return format_response(success=False, data=data, message=message, status_code=status_code)
