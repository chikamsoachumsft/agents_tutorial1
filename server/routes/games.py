from flask import jsonify, Response, Blueprint, request
from models import db, Game, Publisher, Category
from sqlalchemy.orm import Query
from sqlalchemy.exc import IntegrityError

# Create a Blueprint for games routes
games_bp = Blueprint('games', __name__)

def get_games_base_query() -> Query:
    return db.session.query(Game).join(
        Publisher, 
        Game.publisher_id == Publisher.id, 
        isouter=True
    ).join(
        Category, 
        Game.category_id == Category.id, 
        isouter=True
    )

@games_bp.route('/api/games', methods=['GET'])
def get_games() -> Response:
    # Use the base query for all games
    games_query = get_games_base_query().all()
    
    # Convert the results using the model's to_dict method
    games_list = [game.to_dict() for game in games_query]
    
    return jsonify(games_list)

@games_bp.route('/api/games/<int:id>', methods=['GET'])
def get_game(id: int) -> tuple[Response, int] | Response:
    # Use the base query and add filter for specific game
    game_query = get_games_base_query().filter(Game.id == id).first()
    
    # Return 404 if game not found
    if not game_query: 
        return jsonify({"error": "Game not found"}), 404
    
    # Convert the result using the model's to_dict method
    game = game_query.to_dict()
    
    return jsonify(game)

@games_bp.route('/api/games', methods=['POST'])
def create_game() -> tuple[Response, int]:
    """Create a new game"""
    try:
        # Get JSON data from request
        data = request.get_json(force=True, silent=True)
        
        # Validate data exists
        if data is None:
            return jsonify({"error": "No data provided"}), 400
        
        if not data:  # Empty dict
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['title', 'description', 'publisher_id', 'category_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Validate publisher exists
        publisher = Publisher.query.get(data['publisher_id'])
        if not publisher:
            return jsonify({"error": "Publisher not found"}), 400
        
        # Validate category exists
        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({"error": "Category not found"}), 400
        
        # Create new game
        new_game = Game(
            title=data['title'],
            description=data['description'],
            publisher_id=data['publisher_id'],
            category_id=data['category_id'],
            star_rating=data.get('star_rating')  # Optional field
        )
        
        # Add to database
        db.session.add(new_game)
        db.session.commit()
        
        # Return the created game with relationships loaded
        created_game = get_games_base_query().filter(Game.id == new_game.id).first()
        return jsonify(created_game.to_dict()), 201
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred"}), 500

@games_bp.route('/api/games/<int:id>', methods=['PUT'])
def update_game(id: int) -> tuple[Response, int]:
    """Update an existing game"""
    try:
        # Find the game to update
        game = Game.query.get(id)
        if not game:
            return jsonify({"error": "Game not found"}), 404
        
        # Get JSON data from request
        data = request.get_json(force=True, silent=True)
        if data is None:
            return jsonify({"error": "No data provided"}), 400
        
        if not data:  # Empty dict
            return jsonify({"error": "No data provided"}), 400
        
        # Update fields if provided
        if 'title' in data:
            game.title = data['title']
        
        if 'description' in data:
            game.description = data['description']
        
        if 'publisher_id' in data:
            # Validate publisher exists
            publisher = Publisher.query.get(data['publisher_id'])
            if not publisher:
                return jsonify({"error": "Publisher not found"}), 400
            game.publisher_id = data['publisher_id']
        
        if 'category_id' in data:
            # Validate category exists
            category = Category.query.get(data['category_id'])
            if not category:
                return jsonify({"error": "Category not found"}), 400
            game.category_id = data['category_id']
        
        if 'star_rating' in data:
            game.star_rating = data['star_rating']
        
        # Save changes
        db.session.commit()
        
        # Return the updated game with relationships loaded
        updated_game = get_games_base_query().filter(Game.id == id).first()
        return jsonify(updated_game.to_dict()), 200
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred"}), 500

@games_bp.route('/api/games/<int:id>', methods=['DELETE'])
def delete_game(id: int) -> tuple[Response, int]:
    """Delete a game"""
    try:
        # Find the game to delete
        game = Game.query.get(id)
        if not game:
            return jsonify({"error": "Game not found"}), 404
        
        # Delete the game
        db.session.delete(game)
        db.session.commit()
        
        return jsonify({"message": "Game deleted successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred"}), 500
