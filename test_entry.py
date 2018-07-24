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
        self.register_data = json.dumps(dict({
            "username":"erick",
            "email":"erick@gmail.com",
            "password":"password"
            }))

        self.register_result = self.app.post("/api/auth/register/",
                                                data=self.register_data,
                                                content_type='application/json')
        self.login_data = json.dumps(dict({
            "email": "erick@gmail.com",
            "password": "password"
        }))
        self.login_result = self.app.post("/api/auth/login/",
                                               data=self.login_data,
                                               content_type="application/json")
        self.access_token = json.loads(
        self.login_result.data.decode('utf-8'))['access_token']
        self.headers = dict(Authorization= self.access_token,
                            content_type="application/json")
    def create(self, owner="erick", title="a good day in space"):
        """This helper method helps register a test user."""
        diary_data = {'owner': owner, 'title': title}
        return self.app.post(
                '/api/v1/entries/',
                headers=self.headers,
                data=json.dumps(diary_data))
    
    def test_diary_entry(self):
        """
        Test a diary entry
        """
        result = self.app.post("/api/v1/entries/", data=self.entry_data,
                                    headers=self.headers)
        self.assertEqual(result.status_code, 201)

    def test_entry_without_owner(self):
        """Test if an entry can be created without an owner"""
        entry_res = self.create("", "a walk in the park")
        result = json.loads(entry_res.data.decode())
        self.assertEqual(result['error'], "provide entry owner")
        self.assertEqual(entry_res.status_code, 400)

    def test_create_entry_without_username(self):
        """
        
        """
        result = self.app.post('/api/v1/entries/', headers=self.headers, data={
            'owner': "",
            'title':"a day in the park"
        })
        self.assertEqual(result.status_code, 400)
    def test_entry_without_title(self):
        """Test if an entry can be created without a title"""
        entry_res = self.create("erick", "")
        result = json.loads(entry_res.data.decode())
        self.assertEqual(result['error'], "provide the title for the entry")
        self.assertEqual(entry_res.status_code, 400)

    def test_if_entry_is_created(self):
        """
        Test new entry creation
        """
        entry_res = self.create()
        result = json.loads(entry_res.data.decode())
        self.assertEqual(entry_res.status_code, 201)

    def test_if_entry_exists(self):
        """Test that a user cannot create an entry twice"""
        self.create("erick", "a walk in the park")
        second_res = self.create("erick", "a walk in the park")
        result = json.loads(second_res.data.decode())
        self.assertEqual(result['error'],
                         "That item exists")
        self.assertEqual(second_res.status_code, 400)

    def test_get_all_entries(self):
        """Test API to get entries (GET request)."""
        result = self.app.get('/api/v1/entries/', headers=self.headers)
        self.assertEqual(result.status_code, 200)
        self.assertIn('A day in space', result.data.decode('utf-8'))

    def test_empty_post_entries(self):

        """Test bad request on post method"""
        empty = self.app.post("/api/v1/entries/", data={},
                                    content_type="application/json")

        self.assertEqual(empty.status_code, 400)
    def test_edit_an_entry(self):
        """Test API to edit an existing diary entry (PUT request)"""
        entry_res = self.create('erick', 'go to the park')
        result = json.loads(entry_res.data.decode())
        self.assertEqual(entry_res.status_code, 201)

        results = self.app.put('/api/v1/entries/1/', data={
            'owner':'erick',
            'title' :'go to the park and the lounge'
        },headers=self.headers)
        self.assertEqual(results.status_code, 201)

        endresult = self.app.get('/api/v1/entries/1/', headers=self.headers)
        self.assertIn('go to the park and the lounge', endresult.data.decode('utf-8'))

    def test_get_all_diary_entries(self):
        """Test API to get  diary entries (GET request)."""
        result = self.app.post("/api/v1/entries/", data={
            'owner':'erick',
            'title' :'play the guitar and the piano'
        }, content_type="application/json")
        self.assertEqual(result.status_code, 201)

        results = self.app.get('/api/v1/entries/', headers=self.headers)
        self.assertEqual(result.status_code, 200)

    def test_contents_creation(self):
        """
        Test a contents added
        """
        result = self.app.post("/api/v1/entries/1/contents/",
         data={'diary_id':'1', 'contents':'very good contents'},
                                    headers=self.headers)
        self.assertEqual(result.status_code, 201)

if __name__ == "__main__":
    unittest.main()