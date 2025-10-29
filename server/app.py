import os
import logging
from flask import Flask
from flask_cors import CORS

# Import only once - remove duplicate
from utils.database import init_db
from routes.games import games_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get the server directory path
base_dir: str = os.path.abspath(os.path.dirname(__file__))

def create_app(config: dict = None) -> Flask:
    """
    Application factory for creating and configuring the Flask app.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Apply configuration
    app.config['ENV'] = os.getenv('FLASK_ENV', 'development')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    if config:
        app.config.update(config)
    
    # Enable CORS for API endpoints
    CORS(app)
    
    # Initialize the database with the app
    try:
        init_db(app)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    # Register blueprints
    app.register_blueprint(games_bp)
    logger.info("Blueprints registered successfully")
    
    return app


# Create app instance
app: Flask = create_app()

if __name__ == '__main__':
    try:
        port: int = int(os.getenv('PORT', 5100))
        app.run(
            debug=app.config.get('DEBUG', False),
            port=port,
            host='0.0.0.0'  # Allow external connections
        )
    except ValueError:
        logger.error("Invalid PORT environment variable")
        raise
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise
