import unittest
from kisseklyv import app, db

class KisseModelTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()
        app.testing = True
        app.config["SQLALCHEMY_DATABASE_URI"]  = "sqlite://"
        db.create_all()

        self.client.post("/kisse?description=testkisse")
        self.client.post("/person?name=Adam&kisse_id=1")

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_post_expense(self):
        response = self.client.post("/expense?description=Mat&amount=10&person_id=1")
        expected_response = {
            "object_type": "expense",
            "id": 1,
            "description": "Mat",
            "amount": 10,
            "person_id": 1
        }
        self.assertEqual("201 CREATED", response.status)
        self.assertEqual(expected_response,
                         response.get_json())

    def test_post_invalid_expense(self):
        response = self.client.post("/expense?description=Mat&amount=10&person_id=11")
        self.assertEqual("400 BAD REQUEST", response.status)

    def test_put_expense(self):
        post_response = self.client.post("/expense?description=Mat&amount=10&person_id=1")
        expense_id = post_response.get_json()["id"]
        self.client.put(f"/expense?id={expense_id}&amount=20")
        get_response = self.client.get(f"/expense?id={expense_id}")
        self.assertEqual(20, get_response.get_json()["amount"])

        self.client.put(f"/expense?id={expense_id}&description=Dryck")
        get_response = self.client.get(f"/expense?id={expense_id}")
        self.assertEqual("Dryck", get_response.get_json()["description"])

        self.client.put(f"/expense?id={expense_id}&description=Fika&amount=30")
        get_response = self.client.get(f"/expense?id={expense_id}")
        self.assertEqual("Fika", get_response.get_json()["description"])
        self.assertEqual(30, get_response.get_json()["amount"])

    def test_get_expense(self):
        post_response = self.client.post("/expense?description=Mat&amount=10&person_id=1")
        expense_id = post_response.get_json()["id"]
        get_response = self.client.get(f"/expense?id={expense_id}")
        expected_response = {
            "object_type": "expense",
            "id": expense_id,
            "description": "Mat",
            "amount": 10,
            "person_id": 1
        }
        self.assertEqual(expected_response, get_response.get_json())

    def test_get_invalid_expense(self):
        get_response = self.client.get(f"/expense?id=11")
        self.assertEqual("404 NOT FOUND", get_response.status)

    def test_delete_expense(self):
        post_response = self.client.post("/expense?description=Mat&amount=10&person_id=1")
        expense_id = post_response.get_json()["id"]
        delete_response = self.client.delete(f"/expense?id={expense_id}")
        self.assertEqual("204 NO CONTENT", delete_response.status)
        get_response = self.client.get(f"/expense?id={expense_id}")
        self.assertEqual("404 NOT FOUND", get_response.status)

    def test_delete_invalid_expense(self):
        delete_response = self.client.delete(f"/expense?id=11")
        self.assertEqual("404 NOT FOUND", delete_response.status)
