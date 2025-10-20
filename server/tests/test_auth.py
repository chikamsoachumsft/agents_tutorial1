import unittest
import json
from typing import Dict, Any
from flask import Flask, Response
from models import User, db, init_db
from routes.auth import auth_bp
from routes.users import users_bp

class TestAuthRoutes(unittest.TestCase):
    # Test data
    TEST_USER: Dict[str, str] = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    TEST_USER_2: Dict[str, str] = {
        "email": "test2@example.com",
        "password": "testpass456"
    }
    
    # API paths
    REGISTER_PATH: str = '/api/v1/auth/register'
    LOGIN_PATH: str = '/api/v1/auth/login'
    LOGOUT_PATH: str = '/api/v1/auth/logout'
    REFRESH_PATH: str = '/api/v1/auth/refresh'
    PROFILE_PATH: str = '/api/v1/users/profile'
    DELETE_ACCOUNT_PATH: str = '/api/v1/users/account'

    def setUp(self) -> None:
        """Set up test database and seed data"""
        # Create a fresh Flask app for testing
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Register blueprints
        self.app.register_blueprint(auth_bp)
        self.app.register_blueprint(users_bp)
        
        # Initialize the test client
        self.client = self.app.test_client()
        
        # Initialize in-memory database for testing
        init_db(self.app, testing=True)
        
        # Create tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self) -> None:
        """Clean up test database and ensure proper connection closure"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def _get_response_data(self, response: Response) -> Any:
        """Helper method to parse response data"""
        return json.loads(response.data)
    
    def _register_user(self, email: str = None, password: str = None) -> Response:
        """Helper method to register a user"""
        user_data = {
            "email": email or self.TEST_USER["email"],
            "password": password or self.TEST_USER["password"]
        }
        return self.client.post(
            self.REGISTER_PATH,
            data=json.dumps(user_data),
            content_type='application/json'
        )
    
    def _login_user(self, email: str = None, password: str = None) -> Response:
        """Helper method to login a user"""
        user_data = {
            "email": email or self.TEST_USER["email"],
            "password": password or self.TEST_USER["password"]
        }
        return self.client.post(
            self.LOGIN_PATH,
            data=json.dumps(user_data),
            content_type='application/json'
        )

    # Registration Tests
    def test_register_success(self) -> None:
        """Test successful user registration"""
        response = self._register_user()
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "User registered successfully")
        self.assertIn('user', data['data'])
        self.assertIn('accessToken', data['data'])
        self.assertIn('refreshToken', data['data'])
        self.assertEqual(data['data']['user']['email'], self.TEST_USER["email"])
    
    def test_register_duplicate_email(self) -> None:
        """Test registration with duplicate email"""
        # Register first user
        self._register_user()
        
        # Try to register same user again
        response = self._register_user()
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 409)
        self.assertFalse(data['success'])
        self.assertIn("already exists", data['message'])
    
    def test_register_missing_email(self) -> None:
        """Test registration with missing email"""
        response = self.client.post(
            self.REGISTER_PATH,
            data=json.dumps({"password": "testpass123"}),
            content_type='application/json'
        )
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
    
    def test_register_missing_password(self) -> None:
        """Test registration with missing password"""
        response = self.client.post(
            self.REGISTER_PATH,
            data=json.dumps({"email": "test@example.com"}),
            content_type='application/json'
        )
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
    
    def test_register_invalid_email(self) -> None:
        """Test registration with invalid email format"""
        response = self._register_user(email="invalid-email", password="testpass123")
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertIn("email", data['message'].lower())
    
    def test_register_short_password(self) -> None:
        """Test registration with short password"""
        response = self._register_user(email="test@example.com", password="short")
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertIn("8 characters", data['message'])
    
    # Login Tests
    def test_login_success(self) -> None:
        """Test successful user login"""
        # Register user first
        self._register_user()
        
        # Login
        response = self._login_user()
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Login successful")
        self.assertIn('user', data['data'])
        self.assertIn('accessToken', data['data'])
        self.assertIn('refreshToken', data['data'])
    
    def test_login_wrong_password(self) -> None:
        """Test login with wrong password"""
        # Register user
        self._register_user()
        
        # Try to login with wrong password
        response = self._login_user(password="wrongpassword")
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])
        self.assertIn("Invalid", data['message'])
    
    def test_login_nonexistent_user(self) -> None:
        """Test login with non-existent user"""
        response = self._login_user(email="nonexistent@example.com")
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])
    
    def test_login_missing_credentials(self) -> None:
        """Test login with missing credentials"""
        response = self.client.post(
            self.LOGIN_PATH,
            data=json.dumps({}),
            content_type='application/json'
        )
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
    
    # Token Refresh Tests
    def test_refresh_token_success(self) -> None:
        """Test successful token refresh"""
        # Register and get tokens
        register_response = self._register_user()
        register_data = self._get_response_data(register_response)
        refresh_token = register_data['data']['refreshToken']
        
        # Refresh token
        response = self.client.post(
            self.REFRESH_PATH,
            data=json.dumps({"refreshToken": refresh_token}),
            content_type='application/json'
        )
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('accessToken', data['data'])
    
    def test_refresh_token_invalid(self) -> None:
        """Test token refresh with invalid token"""
        response = self.client.post(
            self.REFRESH_PATH,
            data=json.dumps({"refreshToken": "invalid_token"}),
            content_type='application/json'
        )
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])
    
    def test_refresh_token_missing(self) -> None:
        """Test token refresh without token"""
        response = self.client.post(
            self.REFRESH_PATH,
            data=json.dumps({}),
            content_type='application/json'
        )
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
    
    # Logout Tests
    def test_logout_success(self) -> None:
        """Test successful logout"""
        # Register and get token
        register_response = self._register_user()
        register_data = self._get_response_data(register_response)
        access_token = register_data['data']['accessToken']
        
        # Logout
        response = self.client.post(
            self.LOGOUT_PATH,
            headers={'Authorization': f'Bearer {access_token}'}
        )
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
    
    def test_logout_without_token(self) -> None:
        """Test logout without authentication token"""
        response = self.client.post(self.LOGOUT_PATH)
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])
    
    # Profile Tests
    def test_get_profile_success(self) -> None:
        """Test successful profile retrieval"""
        # Register and get token
        register_response = self._register_user()
        register_data = self._get_response_data(register_response)
        access_token = register_data['data']['accessToken']
        
        # Get profile
        response = self.client.get(
            self.PROFILE_PATH,
            headers={'Authorization': f'Bearer {access_token}'}
        )
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('email', data['data'])
        self.assertEqual(data['data']['email'], self.TEST_USER["email"])
    
    def test_get_profile_without_token(self) -> None:
        """Test profile retrieval without token"""
        response = self.client.get(self.PROFILE_PATH)
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])
    
    def test_update_profile_success(self) -> None:
        """Test successful profile update"""
        # Register and get token
        register_response = self._register_user()
        register_data = self._get_response_data(register_response)
        access_token = register_data['data']['accessToken']
        
        # Update profile
        new_email = "newemail@example.com"
        response = self.client.put(
            self.PROFILE_PATH,
            data=json.dumps({"email": new_email}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['email'], new_email)
    
    def test_update_profile_duplicate_email(self) -> None:
        """Test profile update with duplicate email"""
        # Register two users
        self._register_user()
        register_response_2 = self._register_user(
            email=self.TEST_USER_2["email"],
            password=self.TEST_USER_2["password"]
        )
        register_data_2 = self._get_response_data(register_response_2)
        access_token_2 = register_data_2['data']['accessToken']
        
        # Try to update second user's email to first user's email
        response = self.client.put(
            self.PROFILE_PATH,
            data=json.dumps({"email": self.TEST_USER["email"]}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token_2}'}
        )
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 409)
        self.assertFalse(data['success'])
        self.assertIn("already in use", data['message'])
    
    def test_delete_account_success(self) -> None:
        """Test successful account deletion"""
        # Register and get token
        register_response = self._register_user()
        register_data = self._get_response_data(register_response)
        access_token = register_data['data']['accessToken']
        
        # Delete account
        response = self.client.delete(
            self.DELETE_ACCOUNT_PATH,
            headers={'Authorization': f'Bearer {access_token}'}
        )
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        
        # Verify user is deleted by trying to login
        login_response = self._login_user()
        login_data = self._get_response_data(login_response)
        self.assertEqual(login_response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
