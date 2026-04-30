import sqlite3
import pandas as pd

DB_NAME = "expenses.db"


# ----------------------------
# INIT DB (AUTO MIGRATE SAFE)
# ----------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            receipt_text TEXT
        )
    """)

    # SAFE MIGRATION: add missing column if old DB exists
    try:
        c.execute("ALTER TABLE expenses ADD COLUMN receipt_text TEXT")
    except:
        pass

    conn.commit()
    conn.close()


# ----------------------------
# ADD EXPENSE
# ----------------------------
def add_expense(amount, category, receipt_text):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        INSERT INTO expenses (amount, category, receipt_text)
        VALUES (?, ?, ?)
    """, (amount, category, receipt_text))

    conn.commit()
    conn.close()


# ----------------------------
# GET EXPENSES
# ----------------------------
def get_expenses():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    return df


# ----------------------------
# INIT ON IMPORT
# ----------------------------
init_db()