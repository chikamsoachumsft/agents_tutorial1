"""
Publisher model for the Tailspin Toys Crowd Funding platform.

This module defines the Publisher model which represents game publishers
seeking funding for their titles through the crowdfunding platform.
"""
from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship

class Publisher(BaseModel):
    """
    Model representing a game publisher on the crowdfunding platform.
    
    Attributes:
        id (int): Primary key identifier
        name (str): Publisher name (2-100 characters, unique)
        description (str): Publisher description (minimum 10 characters)
        games: Relationship to Game models published by this publisher
    """
    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # One-to-many relationship: one publisher has many games
    games = relationship("Game", back_populates="publisher")

    @validates('name')
    def validate_name(self, key, name):
        """
        Validate publisher name meets minimum length requirements.
        
        Args:
            key (str): The field name being validated
            name (str): The publisher name to validate
            
        Returns:
            str: The validated publisher name
            
        Raises:
            ValueError: If name is too short or invalid
        """
        return self.validate_string_length('Publisher name', name, min_length=2)

    @validates('description')
    def validate_description(self, key, description):
        """
        Validate publisher description meets minimum length requirements.
        
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
        Return string representation of the Publisher object.
        
        Returns:
            str: String representation showing publisher name
        """
        return f'<Publisher {self.name}>'

    def to_dict(self):
        """
        Convert Publisher object to dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary containing publisher data including game count
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'game_count': len(self.games) if self.games else 0
        }