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

    def test_registration(self):
        """
        Test new user registration
        """
        result = self.app.post("/api/auth/register/", data=self.user_data,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 201)

    def test_registration_without_username(self):
        """
        Test that empty user name  cannot register
        """
        test_data = json.dumps(dict({
            "username": "",
            "email": "erick@gmail.com",
            "password": "password"
        }))
        result = self.app.post("/api/auth/register/", data = test_data,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 400)

    def test_registration_without_user_password(self):
        """
        Test that empty user password  cannot register
        """
        test_data = json.dumps(dict({
            "username": "erick",
            "email": "erick@gmail.com",
            "password": ""
        }))
        result = self.app.post("/api/auth/register/", data=test_data,
                                    content_type="application/json")

        self.assertEqual(result.status_code, 400)

    def test_registration_with_special_characters(self):
        """test that user name cannot contain special characters eg @#
        """
        test_data = json.dumps(dict({
            "username":"@erick",
            "email": "erick@email.com",
            "password":"password"
            }))
        result = self.app.post("/api/auth/register/" ,data = test_data,
                            content_type = "application/json")
        self.assertEqual(result.status_code, 403)

    def test_registration_with_invalid_email(self):
        """test that the email supplied by the user is valid
        """
        test_data = json.dumps(dict({
            "username":"erick",
            "email": "erick@emailcom",
            "password":"password"
            }))
        result = self.app.post("/api/auth/register/" ,data = test_data,
                            content_type = "application/json")
        self.assertEqual(result.status_code, 403)

    def test_registration_with_a_short_password(self):
        """test that the email supplied by the user is valid
        """
        test_data = json.dumps(dict({
            "username":"erick",
            "email": "erick@emailcom",
            "password":"pass"
            }))
        result = self.app.post("/api/auth/register/" ,data = test_data,
                            content_type = "application/json")
        self.assertEqual(result.status_code, 403)

    def test_register_with_invalid_url(self):
        """
        Test registration with an invalid url
        """
        result = self.app.post('/api/auth/regist/', data=self.user_data)
        self.assertEqual(result.status_code, 404)

if __name__ == "__main__":
    unittest.main()