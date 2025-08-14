"""
Game model for the Tailspin Toys Crowd Funding platform.

This module defines the Game model which represents games available for
crowdfunding, including their metadata, ratings, and relationships to
publishers and categories.
"""
from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship

class Game(BaseModel):
    """
    Model representing a game available for crowdfunding.
    
    Attributes:
        id (int): Primary key identifier
        title (str): Game title (2-100 characters)
        description (str): Game description (minimum 10 characters)
        star_rating (float): User rating from 0.0 to 5.0
        category_id (int): Foreign key to categories table
        publisher_id (int): Foreign key to publishers table
        category: Relationship to Category model
        publisher: Relationship to Publisher model
    """
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    star_rating = db.Column(db.Float, nullable=True)
    
    # Foreign keys for one-to-many relationships
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'), nullable=False)
    
    # One-to-many relationships (many games belong to one category/publisher)
    category = relationship("Category", back_populates="games")
    publisher = relationship("Publisher", back_populates="games")
    
    @validates('title')
    def validate_name(self, key, name):
        """
        Validate game title meets minimum length requirements.
        
        Args:
            key (str): The field name being validated
            name (str): The title value to validate
            
        Returns:
            str: The validated title
            
        Raises:
            ValueError: If title is too short or invalid
        """
        return self.validate_string_length('Game title', name, min_length=2)
    
    @validates('description')
    def validate_description(self, key, description):
        """
        Validate game description meets minimum length requirements.
        
        Args:
            key (str): The field name being validated
            description (str): The description value to validate
            
        Returns:
            str: The validated description
            
        Raises:
            ValueError: If description is too short or invalid
        """
        if description is not None:
            return self.validate_string_length('Description', description, min_length=10, allow_none=True)
        return description
    
    def __repr__(self):
        """
        Return string representation of the Game object.
        
        Returns:
            str: String representation showing title and ID
        """
        return f'<Game {self.title}, ID: {self.id}>'

    def to_dict(self):
        """
        Convert Game object to dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary containing game data with camelCase keys for frontend
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'publisher': {'id': self.publisher.id, 'name': self.publisher.name} if self.publisher else None,
            'category': {'id': self.category.id, 'name': self.category.name} if self.category else None,
            'starRating': self.star_rating  # Changed from star_rating to starRating
        }