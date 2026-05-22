import sqlite3

def get_connection():
    conn = sqlite3.connect("bank.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        acc_no TEXT UNIQUE,
        pin TEXT,
        balance REAL DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        acc_no TEXT,
        type TEXT,
        amount REAL
    )
    """)

    conn.commit()
    conn.close()