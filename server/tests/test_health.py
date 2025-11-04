import unittest
import json
from typing import Any
from flask import Flask, Response
from routes.health import health_bp

class TestHealthRoutes(unittest.TestCase):
    # API path
    HEALTH_PATH: str = '/api/v1/health/status'

    def setUp(self) -> None:
        """Set up test Flask app"""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        
        # Register blueprint
        self.app.register_blueprint(health_bp)
        
        # Initialize the test client
        self.client = self.app.test_client()

    def _get_response_data(self, response: Response) -> Any:
        """Helper method to parse response data"""
        return json.loads(response.data)

    def test_health_check_success(self) -> None:
        """Test successful health check"""
        response = self.client.get(self.HEALTH_PATH)
        data = self._get_response_data(response)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "API is running")
        self.assertIn('status', data['data'])
        self.assertEqual(data['data']['status'], 'healthy')
        self.assertIn('timestamp', data)

if __name__ == '__main__':
    unittest.main()
