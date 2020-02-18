from kisseklyv import calculate_klyv as klyv
from typing import Dict
from kisseklyv import hashid


def get_kisseklyv(kisse) -> Dict:
    expenses, people = _get_expenses_and_people_from_model(kisse)
    split = klyv.get_split(expenses, people)
    return _get_json_output_from_split(split, kisse)


def _get_expenses_and_people_from_model(kisse):
    people = [person.name for person in kisse.people]
    expenses = []
    for person in kisse.people:
        for expense in person.expenses:
            expenses.append(klyv.Expense(payer=person.name,
                                         amount=expense.amount))
    return expenses, people


def _get_json_output_from_split(split, kisse):
    payments = []
    user_id_name_map = {}
    for person in kisse.people:
        user_id_name_map[person.name] = person.hashid
    for payment in split:
        payments.append({
            "payer_id": user_id_name_map[payment.payer],
            "recipient_id": user_id_name_map[payment.recipient],
            "amount": payment.amount
        })
    output = {
        "object_type": "kisseklyv",
        "kisse_id": kisse.hashid,
        "payments": payments
    }
    return output
