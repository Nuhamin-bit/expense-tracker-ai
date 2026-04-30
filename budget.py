import sqlite3

DB = "expenses.db"


def set_budget(category, limit):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            category TEXT PRIMARY KEY,
            monthly_limit REAL
        )
    """)

    c.execute("""
        INSERT OR REPLACE INTO budgets (category, monthly_limit)
        VALUES (?, ?)
    """, (category, limit))

    conn.commit()
    conn.close()


def get_budgets():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT category, monthly_limit FROM budgets")
    data = c.fetchall()

    conn.close()
    return data


def check_budget_status(category, spent):
    budgets = dict(get_budgets())

    if category not in budgets:
        return None

    limit = budgets[category]
    usage = (spent / limit) * 100

    if usage >= 100:
        return "❌ OVER BUDGET"
    elif usage >= 80:
        return "⚠️ WARNING"
    else:
        return "✅ OK"