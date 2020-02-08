from kisseklyv import calculate_klyv
from kisseklyv import models
from typing import Dict


def get_kisseklyv(kisse: models.Kisse) -> Dict:
    expenses, people = _get_expenses_and_people_from_model(kisse)
    split = calculate_klyv.get_split(expenses, people)
    return _get_json_output_from_split(split, kisse)


def _get_expenses_and_people_from_model(kisse: models.Kisse):
    return None, None


def _get_json_output_from_split(split, kisse):
    return {}
