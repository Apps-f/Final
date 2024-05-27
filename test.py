import unittest
import warnings
import json
from app import app


class HeroesAPITests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p> Hello World </p>")

    def test_get_heroes(self):
        response = self.app.get("/heroes")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(json.loads(response.data), list))

    def test_get_heroes_by_id(self):
        # Assuming hero with ID 1 exists
        response = self.app.get("/heroes/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(json.loads(response.data), list))

    def test_add_heroes(self):
        new_hero = {"name": "Grimstroke", "role": "Support"}
        response = self.app.post("/heroes", data=json.dumps(new_hero), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Hero added successfully" in response.data.decode())

    def test_update_heroes(self):
        update_data = {"name": "Invoker", "role": "Carry"}
        response = self.app.put("/heroes/1", data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Hero updated successfully" in response.data.decode())

    def test_delete_heroes(self):
        response = self.app.delete("/heroes/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Hero deleted successfully" in response.data.decode())


if __name__ == "__main__":
    unittest.main()
