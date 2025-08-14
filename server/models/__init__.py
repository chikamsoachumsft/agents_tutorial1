"""
Database initialization module for the Tailspin Toys Crowd Funding platform.

This module sets up the SQLAlchemy database instance and provides
initialization functions for the database and models.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models after db is defined to avoid circular imports
from .category import Category
from .game import Game
from .publisher import Publisher

def init_db(app, testing: bool = False):
    """
    Initialize the database with the Flask application.
    
    Sets up the SQLAlchemy database instance and creates all tables
    within the application context.
    
    Args:
        app: The Flask application instance to initialize with
        testing (bool): If True, allows reinitialization for testing purposes
    """
    if testing:
        # For testing, we want to be able to reinitialize
        db.init_app(app)
    else:
        try:
            db.init_app(app)
        except RuntimeError:
            # Database already initialized
            pass
    
    # Create tables when initializing
    with app.app_context():
        db.create_all()