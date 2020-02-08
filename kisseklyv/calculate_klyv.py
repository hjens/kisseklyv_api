from typing import Dict, List
from attr import dataclass


class KisseKlyvException(Exception):
    pass


@dataclass
class Expense:
    payer: str
    amount: float


@dataclass
class Payment:
    payer: str
    recipient: str
    amount: float


def _get_initial_debt_levels(expenses: List[Expense],
                             people: List[str]) -> Dict[str, float]:
    debts = {name: 0 for name in people}
    for expense in expenses:
        for name in people:
            if name == expense.payer:
                debts[name] -= (expense.amount - expense.amount / len(people))
            else:
                debts[name] += expense.amount / len(people)
    return debts


def _apply_payment_to_debts(debt_levels: Dict[str, float],
                            payment: Payment) -> Dict[str, float]:
    levels_out = debt_levels.copy()
    levels_out[payment.recipient] += payment.amount
    levels_out[payment.payer] -= payment.amount
    return levels_out


def _are_debts_settled(debt_levels: Dict[str, float]) -> bool:
    abs_sum = sum([abs(level) for level in debt_levels.values()])
    return abs_sum < 1e-9


def _get_next_payment(debt_levels: Dict[str, float]) -> Payment:
    assert len(debt_levels) > 0

    payer = list(debt_levels.keys())[0]
    recipient = payer
    max_level = debt_levels[payer]
    min_level = max_level

    for name, level in debt_levels.items():
        if level > max_level and level != 0:
            max_level = level
            payer = name
        if level < min_level and level != 0:
            min_level = level
            recipient = name
    amount = min(debt_levels[payer], -debt_levels[recipient])
    return Payment(payer=payer, recipient=recipient, amount=amount)


def get_split(expenses: List[Expense], people: List[str]) -> List[Payment]:
    for expense in expenses:
        if expense.amount < 0:
            raise KisseKlyvException("Negative payments not supported")
        if expense.payer not in people:
            raise KisseKlyvException("Expenses contains invalid person")
    if len(people) != len(set(people)):
        raise KisseKlyvException("List contains duplicate people")

    paybacks = []
    debts = _get_initial_debt_levels(expenses, people)
    while not _are_debts_settled(debts):
        payment = _get_next_payment(debts)
        paybacks.append(payment)
        debts = _apply_payment_to_debts(debts, payment)
    return paybacks