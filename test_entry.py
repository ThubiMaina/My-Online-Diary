import unittest
import json
from app import create_app


class EntryTestCase(unittest.TestCase):
    """Test case for the Diary entries"""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name='testing').test_client()
        self.entry_data = json.dumps(dict({
                    "owner": "erick",
                    "title": "A day in space"
                }))
    def register_user(self, email="erick@gmail.com", username="erick",
                      password="password"):
        """This helper method helps register a test user."""
        user_data = {'email': email, 'username': username,
                     'password': password}
        return self.app.post(
                '/api/auth/register/',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(user_data)
               )

    def login_user(self, email="erick@gmail.com", password="password"):
        """This helper method helps log in a test user."""
        user_data = {'email': email, 'password': password}
        return self.app.post(
                '/api/auth/login/',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(user_data)
               )

    def create(self, user_id="1", title="Visit kenya",
        content="Eat lots of nyama choma"):
        """This helper method helps register a test user."""
        self.register_user()
        result = self.login_user()
        diary_data = {'user_id': user_id, 'title': title, 'content':content}
        access_token = json.loads(result.data.decode())['access_token']
        result = self.app.post("/api/v1/entries/", 
                                data=diary_data,
                                headers={'Content-Type': 'application/json',
                         'Authorization': access_token})
        return result

    def test_diary_entry(self):
        """
        Test a diary entry
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        result = self.app.post("/api/v1/entries/", 
                                data=self.entry_data,
                                headers={'Content-Type': 'application/json',
                         'Authorization': access_token})
        res = json.loads(result.data.decode())
        self.assertEqual(result.status_code, 201)
        self.assertEqual(res['message'], "entry created")


    
    def test_get_all_entries(self):
        """Test API to get entries (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        result = self.app.get("/api/v1/entries/", 
                                headers={'Content-Type': 'application/json',
                         'Authorization': access_token})
        self.assertEqual(result.status_code, 200)
        self.assertIn('A day in space', result.data.decode('utf-8'))

    def test_empty_post_entries(self):
        """Test bad request on post method"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        empty = self.app.post("/api/v1/entries/", data={},
                                    headers={'Content-Type': 'application/json',
                         'Authorization': access_token})

        self.assertEqual(empty.status_code, 400)

    def test_get_entry_by_id(self):
        """Test API to get a single entry (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        result = self.app.get("/api/v1/entries/1/", 
                                headers={'Content-Type': 'application/json',
                         'Authorization': access_token})
        self.assertEqual(result.status_code, 200)

    def test_invalid_access_token(self):
        """Test API can check for a valid access token"""
        self.register_user()
        result = self.login_user()
        access_token = "deyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJlcmlja0BnbWFpbC5jb20iLCJleHAiOjE1MzI3ODkwNzAsImlzcyI6Im15ZGlhcnkiLCJpYXQiOjE1MzI3ODcyNzB9.m6kLmdUqf4XLq7TIkb97HCCSjIZLJ8kvmwaOah1BClU"
        post_data = self.app.post("/api/v1/entries/", data={'owner':'erick',
                        'title' :'go to the park'},
                          headers={'Content-Type': 'application/json',
                         'Authorization': access_token})
        result = json.loads(post_data.data.decode())
        self.assertEqual(post_data.status_code, 401)
        self.assertEqual(result['error'], "Invalid token. Please register or login")

    def test_empty_access_token(self):
        """Test API can check for an empty access token"""
        self.register_user()
        result = self.login_user()
        access_token = ""
        post_data = self.app.post("/api/v1/entries/", data={'owner':'erick',
                        'title' :'go to the park'},
                          headers={'Content-Type': 'application/json',
                         'Authorization': access_token})
        result = json.loads(post_data.data.decode())
        self.assertEqual(post_data.status_code, 401)
        self.assertEqual(result['error'], "login required")

if __name__ == "__main__":
    unittest.main()