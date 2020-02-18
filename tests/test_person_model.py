from typing import List
import unittest
from kisseklyv import app, db
from kisseklyv import hashid

ID1 = hashid.get_hashid_from_id(1)
ID11 = hashid.get_hashid_from_id(11)

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

    def get_people_from_kisse(self, kisse_id: str) -> List[str]:
        response = self.client.get(f"/kisse?id={kisse_id}")
        json = response.get_json()
        people = json["people"]
        return [p["name"] for p in people]

    def test_post_valid_person(self):
        self.assertEqual([], self.get_people_from_kisse(kisse_id=ID1))

        response = self.client.post(f"/person?name=Adam&kisse_id={ID1}")
        self.assertEqual("201 CREATED", response.status)
        self.assertEqual(["Adam"], self.get_people_from_kisse(kisse_id=ID1))

        self.client.post(f"/person?name=Bertil&kisse_id={ID1}")
        self.assertEqual(["Adam", "Bertil"],
                         self.get_people_from_kisse(kisse_id=ID1))

    def test_post_invalid_existing_person(self):
        self.client.post(f"/person?name=Cesar&kisse_id={ID1}")
        response = self.client.post(f"/person?name=Cesar&kisse_id={ID1}")
        self.assertEqual("400 BAD REQUEST", response.status)
        self.assertEqual("\"A person with the name Cesar already exists in that Kisse.\"",
                         response.data.decode("utf-8").strip())

    def test_post_invalid_person_nonexisting_kisse(self):
        response = self.client.post(f"/person?name=David&kisse_id={ID11}")
        self.assertEqual("400 BAD REQUEST", response.status)
        self.assertEqual(f"\"No Kisse with id {ID11} exists.\"",
                         response.data.decode("utf-8").strip())

    def test_put_person(self):
        post_response = self.client.post(f"/person?name=Erik&kisse_id={ID1}")
        person_id = post_response.get_json()["id"]
        put_response = self.client.put(f"/person?id={person_id}&name=Filip")
        people = self.get_people_from_kisse(kisse_id=ID1)
        self.assertEqual("200 OK", put_response.status)
        self.assertTrue("Filip" in people)
        self.assertFalse("Erik" in people)

    def test_put_invalid_person(self):
        response = self.client.put(f"/person?name=Filip&id={ID11}")
        self.assertTrue(404, response.status)

    def test_delete_person(self):
        post_response = self.client.post(f"/person?name=Gustav&kisse_id={ID1}")
        self.assertTrue("Gustav" in self.get_people_from_kisse(kisse_id=ID1))

        person_id = post_response.get_json()["id"]
        response = self.client.delete(f"/person?id={person_id}")
        self.assertFalse("Gustav" in self.get_people_from_kisse(kisse_id=ID1))
        self.assertEqual("204 NO CONTENT", response.status)

    def test_delete_invalid_person(self):
        response = self.client.delete(f"/person?id={ID11}")
        self.assertEqual("404 NOT FOUND", response.status)

    def test_get_person(self):
        post_response = self.client.post(f"/person?name=Helge&kisse_id={ID1}")
        person_id = post_response.get_json()["id"]

        get_response = self.client.get(f"/person?id={person_id}")
        expected_response = {"object_type": "person",
                             "id": person_id,
                             "kisse_id": ID1,
                             "name": "Helge"}
        self.assertEqual(expected_response, get_response.get_json())
        self.assertEqual("200 OK", get_response.status)

    def test_get_invalid_person(self):
        response = self.client.get(f"/person?id={ID11}")
        self.assertEqual("404 NOT FOUND", response.status)
