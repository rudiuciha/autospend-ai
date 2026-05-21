import sqlite3
from datetime import datetime
from typing import List, Optional
from .models import Expense

DB_PATH = "expenses.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            merchant TEXT NOT NULL,
            category TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            date TEXT NOT NULL,
            raw_text TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_expense(data: dict) -> Expense:
    conn = get_connection()
    now = datetime.now().isoformat()
    cur = conn.execute(
        """INSERT INTO expenses (amount, merchant, category, payment_method, date, raw_text, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (data["amount"], data["merchant"], data["category"],
         data["payment_method"], data["date"], data["raw_text"], now)
    )
    conn.commit()
    expense_id = cur.lastrowid
    conn.close()
    return Expense(id=expense_id, created_at=now, **data)


def get_all_expenses() -> List[Expense]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM expenses ORDER BY created_at DESC").fetchall()
    conn.close()
    return [Expense(**dict(row)) for row in rows]


def get_summary() -> dict:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM expenses").fetchall()
    conn.close()

    total = 0.0
    by_category = {}
    by_payment = {}

    for row in rows:
        r = dict(row)
        total += r["amount"]
        cat = r["category"]
        pm = r["payment_method"]
        by_category[cat] = by_category.get(cat, 0.0) + r["amount"]
        by_payment[pm] = by_payment.get(pm, 0.0) + r["amount"]

    return {
        "total_expenses": total,
        "total_transactions": len(rows),
        "by_category": by_category,
        "by_payment_method": by_payment,
    }
