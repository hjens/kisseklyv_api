import unittest
from kisseklyv import kisseklyv_model
from kisseklyv import models
from kisseklyv import calculate_klyv as klyv
from kisseklyv import app, db
from kisseklyv import hashid

ID1 = hashid.get_hashid_from_id(1)
ID11 = hashid.get_hashid_from_id(11)

class TestKisseklyvModel(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()
        app.testing = True
        app.config["SQLALCHEMY_DATABASE_URI"]  = "sqlite://"
        db.create_all()

        self.client.post("/kisse?description=testkisse")
        self.client.post(f"/person?name=Adam&kisse_id={ID1}")

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_get_kisseklyv_resource(self):
        self.client.post("/kisse?description=middag")
        self.client.post(f"/person?name=Adam&kisse_id={ID1}")
        self.client.post(f"/person?name=Bertil&kisse_id={ID1}")
        self.client.post(f"/person?name=Cesar&kisse_id={ID1}")
        self.client.post(f"/expense?person_id={ID1}&amount=150&description=Mat")
        klyv_response = self.client.get(f"/kisseklyv?kisse_id={ID1}")
        expected_output = {
            "object_type": "kisseklyv",
            "kisse_id": ID1,
            "payments": [
                {"payer_id": hashid.get_hashid_from_id(2),
                 "recipient_id": hashid.get_hashid_from_id(1),
                 "payer_name": "Bertil",
                 "recipient_name": "Adam",
                 "amount": 50},
                {"payer_id": hashid.get_hashid_from_id(3),
                 "recipient_id": hashid.get_hashid_from_id(1),
                 "payer_name": "Cesar",
                 "recipient_name": "Adam",
                 "amount": 50}
            ]
        }
        self.assertEqual(expected_output, klyv_response.get_json())
        self.assertEqual("200 OK", klyv_response.status)

    def test_get_kisseklyv(self):
        kisse = models.Kisse(id=1,
                             description="Testkisse",
                             people=[
                                 models.Person(id=1,
                                               name="Adam",
                                               kisse_id=1,
                                               expenses=[
                                                   models.Expense(
                                                       id=1,
                                                       description="Mat",
                                                       amount=10,
                                                       person_id=1
                                                   )
                                               ]),

                                 models.Person(id=2,
                                               name="Bertil",
                                               kisse_id=1,
                                               expenses=[]
                                               )
                             ])
        expected_output = {
            "object_type": "kisseklyv",
            "kisse_id": ID1,
            "payments": [
                {"payer_id": hashid.get_hashid_from_id(2),
                 "recipient_id": hashid.get_hashid_from_id(1),
                 "payer_name": "Bertil",
                 "recipient_name": "Adam",
                 "amount": 5}
            ]
        }
        output = kisseklyv_model.get_kisseklyv(kisse)
        self.assertEqual(expected_output, output)

    def test_get_invalid_kisseklyv(self):
        output = self.client.get(f"/kisseklyv?kisse_id={ID11}")
        self.assertEqual("404 NOT FOUND", output.status)

    def test_get_expenses_and_people_from_model(self):
        kisse = models.Kisse(id=1,
                             description="Testkisse",
                             people=[
                                 models.Person(id=1,
                                               name="Adam",
                                               kisse_id=1,
                                               expenses=[
                                                   models.Expense(
                                                       id=1,
                                                       description="Mat",
                                                       amount=10,
                                                       person_id=1
                                                   ),
                                                   models.Expense(
                                                       id=2,
                                                       description="Dryck",
                                                       amount=2,
                                                       person_id=1
                                                   )
                                               ]),

                                 models.Person(id=2,
                                               name="Bertil",
                                               kisse_id=1,
                                               expenses=[
                                                   models.Expense(
                                                       id=3,
                                                       description="Diverse",
                                                       amount=3,
                                                       person_id=2
                                                   )
                                                   ]
                                               )
                             ])
        expected_expenses = [klyv.Expense(payer="Adam", amount=10),
                             klyv.Expense(payer="Adam", amount=2),
                             klyv.Expense(payer="Bertil", amount=3)]
        expected_people = ["Adam", "Bertil"]
        expenses, people = kisseklyv_model._get_expenses_and_people_from_model(kisse)
        self.assertEqual(expected_expenses, expenses)
        self.assertEqual(expected_people, people)

    def test_get_json_output_from_split(self):
        kisse = models.Kisse(
            id=1,
            people = [
                models.Person(id=1,
                              name="Adam",
                              kisse_id=1,
                              expenses=[
                                  models.Expense(
                                      id=1,
                                      description="Mat",
                                      amount=10,
                                      person_id=1
                                  )
                              ]),

                models.Person(id=2,
                              name="Bertil",
                              kisse_id=1,
                              expenses=[]
                              )
            ]
        )
        split = [
            klyv.Payment(
                payer="Bertil",
                recipient="Adam",
                amount=5
            )
        ]
        expected_output = {
            "object_type": "kisseklyv",
            "kisse_id": ID1,
            "payments": [
                {"payer_id": hashid.get_hashid_from_id(2),
                 "recipient_id": hashid.get_hashid_from_id(1),
                 "payer_name": "Bertil",
                 "recipient_name": "Adam",
                 "amount": 5}
            ]
        }
        output = kisseklyv_model._get_json_output_from_split(split, kisse)
        self.assertEqual(expected_output, output)

