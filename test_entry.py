import unittest
import json
from app import create_app


class EntryTestCase(unittest.TestCase):
    """Test case for the Diary entries"""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app('testing').test_client()
        self.headers={'Content-Type': 'application/json'}
        self.entry_data = json.dumps(dict({
                    "owner": "erick",
                    "title": "A day in space"
                }))

    def create(self, owner="erick", title="a good day in space"):
        """This helper method helps register a test user."""
        diary_data = {'owner': owner, 'title': title}
        return self.app.post(
                '/api/v1/entries/',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(diary_data))

    def test_diary_entry(self):
        """
        Test a diary entry
        """
        result = self.app.post("/api/v1/entries/", data=self.entry_data,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 201)

    def test_entry_without_owner(self):
        """Test if an entry can be created without an owner"""
        entry_res = self.create("", "a walk in the park")
        result = json.loads(entry_res.data.decode())
        self.assertEqual(result['error'], "provide entry owner")
        self.assertEqual(entry_res.status_code, 400)

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
        res = self.create()
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)

    def test_if_entry_exists(self):
        """Test that a user cannot vreate an entry twice"""
        self.create("erick", "a walk in the park")
        second_res = self.create("erick", "a walk in the park")
        result = json.loads(second_res.data.decode())
        self.assertEqual(result['error'],
                         "That item exists")
        self.assertEqual(second_res.status_code, 400)
        
if __name__ == "__main__":
    unittest.main()