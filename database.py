import sqlite3

DB_NAME = "expenses.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # expenses table
    c.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            receipt_text TEXT
        )
    """)

    # budgets table (NEW)
    c.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            category TEXT PRIMARY KEY,
            limit_amount REAL
        )
    """)

    conn.commit()
    conn.close()


def add_expense(amount, category, receipt_text):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        INSERT INTO expenses (amount, category, receipt_text)
        VALUES (?, ?, ?)
    """, (amount, category, receipt_text))

    conn.commit()
    conn.close()


def get_expenses():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT amount, category FROM expenses")
    data = c.fetchall()

    conn.close()
    return data


# ---------------- BUDGET FUNCTIONS ----------------

def set_budget(category, limit_amount):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        INSERT OR REPLACE INTO budgets (category, limit_amount)
        VALUES (?, ?)
    """, (category, limit_amount))

    conn.commit()
    conn.close()


def get_budgets():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT category, limit_amount FROM budgets")
    data = c.fetchall()

    conn.close()
    return dict(data)