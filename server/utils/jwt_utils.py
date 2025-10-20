import jwt
import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

def get_jwt_secret() -> str:
    """Get JWT secret from environment or use default for development"""
    return os.getenv('JWT_SECRET', 'dev-secret-key-change-in-production')

def get_jwt_algorithm() -> str:
    """Get JWT algorithm"""
    return 'HS256'

def generate_token(user_id: int, expires_in_hours: int = 24) -> str:
    """
    Generate a JWT token for a user
    
    Args:
        user_id: The user's ID
        expires_in_hours: Token expiration time in hours (default: 24)
    
    Returns:
        JWT token string
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=expires_in_hours),
        'iat': datetime.now(timezone.utc)
    }
    
    token = jwt.encode(payload, get_jwt_secret(), algorithm=get_jwt_algorithm())
    return token

def generate_refresh_token(user_id: int) -> str:
    """
    Generate a refresh token with longer expiration (7 days)
    
    Args:
        user_id: The user's ID
    
    Returns:
        JWT refresh token string
    """
    return generate_token(user_id, expires_in_hours=24 * 7)

def verify_token(token: str) -> Optional[Dict]:
    """
    Verify and decode a JWT token
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, get_jwt_secret(), algorithms=[get_jwt_algorithm()])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_user_id_from_token(token: str) -> Optional[int]:
    """
    Extract user ID from a valid token
    
    Args:
        token: JWT token string
    
    Returns:
        User ID if token is valid, None otherwise
    """
    payload = verify_token(token)
    if payload:
        return payload.get('user_id')
    return None
