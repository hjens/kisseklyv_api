import unittest
from kisseklyv import kisseklyv_model
from kisseklyv import models
from kisseklyv import calculate_klyv as klyv

class TestKisseklyvModel(unittest.TestCase):

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
            "kisse_id": 1,
            "payments": [
                {"payer_id": 2,
                 "recipient_id": 1,
                 "amount": 5}
            ]
        }
        output = kisseklyv_model.get_kisseklyv(kisse)
        self.assertEqual(expected_output, output)

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
                                                   )
                                               ]),

                                 models.Person(id=2,
                                               name="Bertil",
                                               kisse_id=1,
                                               expenses=[]
                                               )
                             ])
        expected_expenses = [klyv.Expense(payer="Adam", amount=10)]
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
            "kisse_id": 1,
            "payments": [
                {"payer_id": 2,
                 "recipient_id": 1,
                 "amount": 5}
            ]
        }
        output = kisseklyv_model._get_json_output_from_split(split, kisse)
        self.assertEqual(expected_output, output)

