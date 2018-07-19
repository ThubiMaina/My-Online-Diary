import unittest
import json
from app import create_app


class UserTestCase(unittest.TestCase):
    """Test case for the user creation and login"""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app('testing').test_client()
        self.user_data = json.dumps(dict({
                    "username": "erick",
                    "email": "erick@gmail.com",
                    "password": "password"
                }))

    
if __name__ == "__main__":
    unittest.main()