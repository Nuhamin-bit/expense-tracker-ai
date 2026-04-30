import sqlite3
import pandas as pd

conn = sqlite3.connect("expenses.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text BLOB,
    category TEXT,
    amount REAL,
    date TEXT
)
""")

def insert_expense(text, category, amount, date):
    cursor.execute(
        "INSERT INTO expenses (text, category, amount, date) VALUES (?, ?, ?, ?)",
        (text, category, amount, date)
    )
    conn.commit()

def get_expenses():
    return pd.read_sql_query("SELECT * FROM expenses", conn)