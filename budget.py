from database import get_expenses, get_budgets


def check_budget_alerts():
    expenses = get_expenses()
    budgets = dict(get_budgets())

    totals = {}

    for amount, category in expenses:
        totals[category] = totals.get(category, 0) + amount

    alerts = []

    for category, total in totals.items():
        limit = budgets.get(category)

        if limit and total > limit:
            alerts.append(f"{category} OVER BUDGET: ${total} / ${limit}")

    return alerts