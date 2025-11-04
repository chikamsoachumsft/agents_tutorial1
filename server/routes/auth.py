from flask import Blueprint, request, Response
from models import db, User
from utils.jwt_utils import generate_token, generate_refresh_token, get_user_id_from_token
from utils.response_formatter import success_response, error_response
from utils.auth_middleware import require_auth
from typing import Tuple

# Create a Blueprint for auth routes
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/v1/auth/register', methods=['POST'])
def register() -> Tuple[Response, int]:
    """
    Register a new user
    
    Request body:
        {
            "email": "user@example.com",
            "password": "password123"
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Request body is required", 400)
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return error_response("Email and password are required", 400)
        
        # Check if user already exists
        existing_user = db.session.query(User).filter(User.email == email.strip().lower()).first()
        if existing_user:
            return error_response("User with this email already exists", 409)
        
        # Create new user
        user = User(email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Generate tokens
        access_token = generate_token(user.id)
        refresh_token = generate_refresh_token(user.id)
        
        return success_response(
            data={
                'user': user.to_dict(),
                'accessToken': access_token,
                'refreshToken': refresh_token
            },
            message="User registered successfully",
            status_code=201
        )
        
    except ValueError as e:
        db.session.rollback()
        return error_response(str(e), 400)
    except Exception as e:
        db.session.rollback()
        return error_response("An error occurred during registration", 500)

@auth_bp.route('/api/v1/auth/login', methods=['POST'])
def login() -> Tuple[Response, int]:
    """
    Authenticate a user and return JWT tokens
    
    Request body:
        {
            "email": "user@example.com",
            "password": "password123"
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Request body is required", 400)
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return error_response("Email and password are required", 400)
        
        # Find user by email
        user = db.session.query(User).filter(User.email == email.strip().lower()).first()
        
        if not user or not user.check_password(password):
            return error_response("Invalid email or password", 401)
        
        # Generate tokens
        access_token = generate_token(user.id)
        refresh_token = generate_refresh_token(user.id)
        
        return success_response(
            data={
                'user': user.to_dict(),
                'accessToken': access_token,
                'refreshToken': refresh_token
            },
            message="Login successful"
        )
        
    except Exception as e:
        return error_response("An error occurred during login", 500)

@auth_bp.route('/api/v1/auth/refresh', methods=['POST'])
def refresh() -> Tuple[Response, int]:
    """
    Refresh access token using refresh token
    
    Request body:
        {
            "refreshToken": "jwt_refresh_token"
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Request body is required", 400)
        
        refresh_token = data.get('refreshToken')
        
        if not refresh_token:
            return error_response("Refresh token is required", 400)
        
        # Verify refresh token
        user_id = get_user_id_from_token(refresh_token)
        
        if not user_id:
            return error_response("Invalid or expired refresh token", 401)
        
        # Get user
        user = db.session.query(User).filter(User.id == user_id).first()
        
        if not user:
            return error_response("User not found", 404)
        
        # Generate new access token
        access_token = generate_token(user.id)
        
        return success_response(
            data={
                'accessToken': access_token
            },
            message="Token refreshed successfully"
        )
        
    except Exception as e:
        return error_response("An error occurred during token refresh", 500)

@auth_bp.route('/api/v1/auth/logout', methods=['POST'])
@require_auth
def logout() -> Tuple[Response, int]:
    """
    Logout user (client should discard tokens)
    Requires authentication header
    """
    return success_response(
        message="Logout successful"
    )
