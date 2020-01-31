import unittest
from kisseklyv import app, db

class KisseModelTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()
        app.testing = True
        app.config["SQLALCHEMY_DATABASE_URI"]  = "sqlite://"
        db.create_all()

        self.client.post("/kisse?description=testkisse")

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_get_existing_kisse(self):
        response = self.client.get("/kisse?kisse_id=1")
        expected_response = {"message": "Get Kisse",
                             "data": {"kisse_id": 1,
                                      "description": "testkisse",
                                      "people": []}}
        self.assertEqual(expected_response, response.get_json())
        self.assertEqual("200 OK", response.status)

    def test_get_nonexisting_kisse(self):
        response = self.client.get("/kisse?kisse_id=11")
        self.assertEqual("404 NOT FOUND", response.status)

    def test_post_kisse(self):
        response = self.client.post("/kisse?description=testkisse2")
        expected_response = {"message": "Kisse created",
                             "data": {"kisse_id": 2,
                                      "description": "testkisse2",
                                      "people": []}}
        self.assertEqual(expected_response, response.get_json())
        self.assertEqual("201 CREATED", response.status)

        response = self.client.get("/kisse?kisse_id=2")
        expected_response = {"message": "Get Kisse",
                             "data": {"kisse_id": 2,
                                      "description": "testkisse2",
                                      "people": []}}
        self.assertEqual(expected_response, response.get_json())
        self.assertEqual("200 OK", response.status)

    def test_put_existing_kisse(self):
        create_response = self.client.post("/kisse?description=nonupdated")
        kisse_id = create_response.get_json()["data"]["kisse_id"]

        response = self.client.put(f"/kisse?kisse_id={kisse_id}&description=updated")
        self.assertEqual("200 OK", response.status)

    def test_put_nonexisting_kisse(self):
        response = self.client.put("/kisse?kisse_id=11&description=updated")
        self.assertEqual("404 NOT FOUND", response.status)

    def test_delete_existing_kisse(self):
        create_response = self.client.post("/kisse?description=todelete")
        kisse_id = create_response.get_json()["data"]["kisse_id"]

        response = self.client.delete(f"/kisse?kisse_id={kisse_id}")
        self.assertEqual("204 NO CONTENT", response.status)

    def test_delete_nonexisting_kisse(self):
        response = self.client.delete("/kisse?kisse_id=11")
        self.assertEqual("404 NOT FOUND", response.status)
