from flask import Blueprint, request, Response
from models import db, User
from utils.response_formatter import success_response, error_response
from utils.auth_middleware import require_auth
from typing import Tuple

# Create a Blueprint for user routes
users_bp = Blueprint('users', __name__)

@users_bp.route('/api/v1/users/profile', methods=['GET'])
@require_auth
def get_profile() -> Tuple[Response, int]:
    """
    Get current user's profile
    Requires authentication header
    """
    try:
        user = request.current_user
        
        return success_response(
            data=user.to_dict(include_timestamps=True),
            message="Profile retrieved successfully"
        )
        
    except Exception as e:
        return error_response("An error occurred while retrieving profile", 500)

@users_bp.route('/api/v1/users/profile', methods=['PUT'])
@require_auth
def update_profile() -> Tuple[Response, int]:
    """
    Update current user's profile (email only for now)
    Requires authentication header
    
    Request body:
        {
            "email": "newemail@example.com"
        }
    """
    try:
        user = request.current_user
        data = request.get_json()
        
        if not data:
            return error_response("Request body is required", 400)
        
        # Update email if provided
        if 'email' in data:
            email = data.get('email')
            if not email:
                return error_response("Email cannot be empty", 400)
            
            # Check if email is already taken by another user
            existing_user = db.session.query(User).filter(
                User.email == email.strip().lower(),
                User.id != user.id
            ).first()
            
            if existing_user:
                return error_response("Email already in use", 409)
            
            user.email = email
        
        db.session.commit()
        
        return success_response(
            data=user.to_dict(include_timestamps=True),
            message="Profile updated successfully"
        )
        
    except ValueError as e:
        db.session.rollback()
        return error_response(str(e), 400)
    except Exception as e:
        db.session.rollback()
        return error_response("An error occurred while updating profile", 500)

@users_bp.route('/api/v1/users/account', methods=['DELETE'])
@require_auth
def delete_account() -> Tuple[Response, int]:
    """
    Delete current user's account
    Requires authentication header
    """
    try:
        user = request.current_user
        
        db.session.delete(user)
        db.session.commit()
        
        return success_response(
            message="Account deleted successfully"
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response("An error occurred while deleting account", 500)
