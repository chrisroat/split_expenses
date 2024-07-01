from split_expenses import Expense, solve_from_expenses

if __name__ == "__main__":
    people = ["Dave", "Chris", "Marc", "Jim"]
    expenses = [
        Expense("Dave", 100, None, None),
        Expense("Chris", 90, None, ["Dave"]),
        Expense("Chris", 40, None, None),
    ]

    status, result = solve_from_expenses(people, expenses)
    print("Status:", status)
    print(result)
