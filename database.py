import sqlite3

DB_NAME = "gym.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():
    with connect() as conn:
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            join_date TEXT NOT NULL,
            fee_paid INTEGER NOT NULL,
            payment_mode TEXT NOT NULL,
            expiry_date TEXT NOT NULL
        )
        """)

        conn.commit()