"""
Base model class for the Tailspin Toys Crowd Funding platform.

This module provides the BaseModel class that serves as the foundation
for all database models, providing common validation functionality.
"""
from . import db

class BaseModel(db.Model):
    """
    Abstract base model class providing common functionality for all models.
    
    This class provides shared validation methods that can be used by
    all model classes to ensure data integrity.
    """
    __abstract__ = True
    
    @staticmethod
    def validate_string_length(field_name, value, min_length=2, allow_none=False):
        """
        Validate that a string field meets length requirements.
        
        Args:
            field_name (str): Name of the field being validated (for error messages)
            value (str or None): The value to validate
            min_length (int): Minimum required length (default: 2)
            allow_none (bool): Whether None values are allowed (default: False)
            
        Returns:
            str or None: The validated value
            
        Raises:
            ValueError: If validation fails
        """
        if value is None:
            if allow_none:
                return value
            else:
                raise ValueError(f"{field_name} cannot be empty")
        
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")
            
        if len(value.strip()) < min_length:
            raise ValueError(f"{field_name} must be at least {min_length} characters")
            
        return value