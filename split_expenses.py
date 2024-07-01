from collections import namedtuple
from itertools import permutations

from pulp import LpVariable, LpMinimize, LpProblem, lpSum, LpInteger, LpStatus

Expense = namedtuple("Expense", ["person", "amount", "include", "exclude"])


def solve_from_expenses(people, expenses):
    balances = calculate_balances(people, expenses)
    return solve_from_balances(balances)


def calculate_balances(people, expenses):
    balances = {person: 0 for person in people}
    for expense in expenses:
        balances[expense.person] += expense.amount

        to_charge = []
        for person in people:
            included = expense.include is None or person in expense.include
            excluded = expense.exclude is not None and person in expense.exclude
            if included and not excluded:
                to_charge.append(person)

        for person in to_charge:
            balances[person] -= expense.amount / len(to_charge)

    return balances


def solve_from_balances(balances):
    people = balances.keys()
    prob = LpProblem("Splitwise", LpMinimize)

    payments = {person: [] for person in people}
    receipts = {person: [] for person in people}
    xfers = []
    for payor, payee in permutations(people, 2):
        amount = LpVariable(f"{payor}_pays_{payee}_amount", 0, None)
        payments[payor].append(amount)
        receipts[payee].append(amount)

        has_xfer = LpVariable(f"{payor}_pays_{payee}", 0, 1, LpInteger)
        prob += has_xfer >= amount * 1e-6
        xfers.append(has_xfer)

    for person in people:
        prob += (lpSum(receipts[person]) - lpSum(payments[person])) == balances[person]

    prob.objective = sum(xfers)
    lp_status = prob.solve()
    status = LpStatus[lp_status]

    result = {}
    for person, person_payments in payments.items():
        for payment in person_payments:
            if payment.value() > 0:
                result[payment.name] = payment.value()

    return status, result
