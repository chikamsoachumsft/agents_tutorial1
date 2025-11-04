"""
Category model for the Tailspin Toys Crowd Funding platform.

This module defines the Category model which represents game categories
used to classify games available for crowdfunding.
"""
from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship

class Category(BaseModel):
    """
    Model representing a game category on the crowdfunding platform.
    
    Attributes:
        id (int): Primary key identifier
        name (str): Category name (2-100 characters, unique)
        description (str): Category description (minimum 10 characters)
        games: Relationship to Game models in this category
    """
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # One-to-many relationship: one category has many games
    games = relationship("Game", back_populates="category")
    
    @validates('name')
    def validate_name(self, key, name):
        """
        Validate category name meets minimum length requirements.
        
        Args:
            key (str): The field name being validated
            name (str): The category name to validate
            
        Returns:
            str: The validated category name
            
        Raises:
            ValueError: If name is too short or invalid
        """
        return self.validate_string_length('Category name', name, min_length=2)
        
    @validates('description')
    def validate_description(self, key, description):
        """
        Validate category description meets minimum length requirements.
        
        Args:
            key (str): The field name being validated
            description (str): The description to validate
            
        Returns:
            str: The validated description
            
        Raises:
            ValueError: If description is too short or invalid
        """
        return self.validate_string_length('Description', description, min_length=10, allow_none=True)
    
    def __repr__(self):
        """
        Return string representation of the Category object.
        
        Returns:
            str: String representation showing category name
        """
        return f'<Category {self.name}>'
        
    def to_dict(self):
        """
        Convert Category object to dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary containing category data including game count
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'game_count': len(self.games) if self.games else 0
        }