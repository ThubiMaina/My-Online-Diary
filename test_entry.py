import unittest
import json
from app import create_app


class EntryTestCase(unittest.TestCase):
    """Test case for the Diary entries"""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app('testing').test_client()
        self.entry_data = json.dumps(dict({
                    "owner": "erick",
                    "title": "A day in space"
                }))

    def test_diary_entry(self):
        """
        Test a diary entry
        """
        result = self.app.post("/api/v1/entries/", data=self.entry_data,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 201)
        
if __name__ == "__main__":
    unittest.main()