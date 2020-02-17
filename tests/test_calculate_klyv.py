import unittest
from kisseklyv import calculate_klyv as klyv
import uuid
import random


class TestCalculateKly(unittest.TestCase):
    def test_simple_split(self):
        expenses = [
            klyv.Expense(payer="Adam",
                         amount=10)
        ]
        people = ["Adam", "Bertil"]
        expected_output = [
            klyv.Payment(payer="Bertil", recipient="Adam", amount=5)
        ]
        output = klyv.get_split(expenses, people)
        self.assertEqual(expected_output, output)

    def test_even_split(self):
        expenses = [
            klyv.Expense(payer="Adam",
                         amount=10),
            klyv.Expense(payer="Bertil",
                         amount=10),
            klyv.Expense(payer="Cesar",
                         amount=10)
        ]
        people = ["Adam", "Bertil", "Cesar"]
        expected_output = []
        output = klyv.get_split(expenses, people)
        self.assertEqual(expected_output, output)

    def test_single_person_split(self):
        expenses = []
        people = ["Adam"]
        expected_output = []
        output = klyv.get_split(expenses, people)
        self.assertEqual(expected_output, output)

    def test_empty_split(self):
        expenses = []
        people = []
        expected_output = []
        output = klyv.get_split(expenses, people)
        self.assertEqual(expected_output, output)

    def test_split_with_negative_payment(self):
        expenses = [
            klyv.Expense(payer="Adam",
                         amount=-10)
        ]
        people = ["Adam", "Bertil"]
        with self.assertRaises(klyv.KisseKlyvException):
            klyv.get_split(expenses, people)

    def test_split_with_duplicate_people(self):
        expenses = [
            klyv.Expense(payer="Adam",
                         amount=10)
        ]
        people = ["Adam", "Bertil", "Adam"]
        with self.assertRaises(klyv.KisseKlyvException):
            klyv.get_split(expenses, people)

    def test_split_with_invalid_payment(self):
        expenses = [
            klyv.Expense(payer="Cesar",
                         amount=10)
        ]
        people = ["Adam", "Bertil"]
        with self.assertRaises(klyv.KisseKlyvException):
            klyv.get_split(expenses, people)

    def test_random_splits(self):
        for i in range(100):
            num_people = random.randint(2, 100)
            num_expenses = random.randint(1, 1000)
            people, expenses, split = self._generate_random_split(num_people, num_expenses)
            self._verify_split(people, expenses, split)
            self._verify_max_num_payments(people, split)

    def _generate_random_split(self, num_people, num_expenses):
        def random_name():
            return str(uuid.uuid4())
        def random_expense(people):
            payer = random.choice(people)
            amount = random.random()*1000
            return klyv.Expense(payer=payer, amount=amount)
        people = [random_name() for _ in range(num_people)]
        expenses = [random_expense(people) for _ in range(num_expenses)]
        return people, expenses, klyv.get_split(expenses, people)

    def _verify_split(self, people, expenses, split):
        money_spent = {p: 0 for p in people}
        for expense in expenses:
            money_spent[expense.payer] += expense.amount

        for payment in split:
            money_spent[payment.payer] += payment.amount
            money_spent[payment.recipient] -= payment.amount

        for i, p in enumerate(people):
            if i > 0:
                diff = money_spent[people[i]] - money_spent[people[i-1]]
                self.assertTrue(diff < 1e-9)

    def _verify_max_num_payments(self, people, split):
        max_num_payments = len(people)-1
        num_payments = {p: 0 for p in people}
        for payment in split:
            num_payments[payment.payer] += 1
        for person in people:
            self.assertTrue(num_payments[person] <= max_num_payments)
