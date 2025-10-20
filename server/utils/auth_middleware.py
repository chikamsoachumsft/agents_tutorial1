from functools import wraps
from flask import request
from models import User, db
from utils.jwt_utils import get_user_id_from_token
from utils.response_formatter import error_response
from typing import Callable, Any

def require_auth(f: Callable) -> Callable:
    """
    Decorator to require authentication for a route
    Extracts token from Authorization header and validates it
    """
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return error_response("Missing authorization header", 401)
        
        # Check for Bearer token format
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return error_response("Invalid authorization header format", 401)
        
        token = parts[1]
        
        # Verify token and get user ID
        user_id = get_user_id_from_token(token)
        
        if not user_id:
            return error_response("Invalid or expired token", 401)
        
        # Get user from database
        user = db.session.query(User).filter(User.id == user_id).first()
        
        if not user:
            return error_response("User not found", 401)
        
        # Add user to request context
        request.current_user = user
        
        return f(*args, **kwargs)
    
    return decorated_function
