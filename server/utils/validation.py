from functools import wraps
from flask import request
from utils.response_formatter import error_response
from typing import Callable, Any, List
import html

def sanitize_string(value: str) -> str:
    """
    Sanitize a string to prevent XSS attacks
    
    Args:
        value: String to sanitize
    
    Returns:
        Sanitized string
    """
    if not isinstance(value, str):
        return value
    
    # HTML escape to prevent XSS
    return html.escape(value.strip())

def sanitize_data(data: Any) -> Any:
    """
    Recursively sanitize data structure
    
    Args:
        data: Data to sanitize (dict, list, or primitive)
    
    Returns:
        Sanitized data
    """
    if isinstance(data, dict):
        return {key: sanitize_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_data(item) for item in data]
    elif isinstance(data, str):
        return sanitize_string(data)
    else:
        return data

def validate_required_fields(required_fields: List[str]) -> Callable:
    """
    Decorator to validate required fields in request JSON
    
    Args:
        required_fields: List of required field names
    
    Returns:
        Decorator function
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args: Any, **kwargs: Any) -> Any:
            data = request.get_json()
            
            if not data:
                return error_response("Request body is required", 400)
            
            missing_fields = [field for field in required_fields if field not in data or not data[field]]
            
            if missing_fields:
                return error_response(
                    f"Missing required fields: {', '.join(missing_fields)}",
                    400
                )
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def sanitize_input(f: Callable) -> Callable:
    """
    Decorator to automatically sanitize request JSON input
    """
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        if request.is_json and request.get_json():
            # Sanitize the JSON data
            original_data = request.get_json()
            sanitized_data = sanitize_data(original_data)
            
            # Replace request data with sanitized version
            request._cached_json = (sanitized_data, sanitized_data)
        
        return f(*args, **kwargs)
    
    return decorated_function
