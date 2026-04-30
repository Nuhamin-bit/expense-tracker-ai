import sqlite3
import pandas as pd

DB = "expenses.db"


def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            receipt_text TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_expense(amount, category, text):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        INSERT INTO expenses (amount, category, receipt_text)
        VALUES (?, ?, ?)
    """, (amount, category, text))

    conn.commit()
    conn.close()


def get_expenses():
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    return df