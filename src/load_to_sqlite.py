"""Load transaction data from CSV into a SQLite database."""

import csv
import sqlite3
from pathlib import Path

CSV_PATH = Path("data/raw/transactions.csv")
DATABASE_PATH = Path("data/transactions.db")


def main() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            category TEXT NOT NULL,
            merchant TEXT NOT NULL,
            country TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)

    with CSV_PATH.open(encoding="utf-8") as file:
        reader = csv.DictReader(file)

        rows = [
            (
                row["transaction_id"],
                row["timestamp"],
                row["category"],
                row["merchant"],
                row["country"],
                float(row["amount"]),
            )
            for row in reader
        ]

    cursor.executemany("""
        INSERT OR REPLACE INTO transactions
        VALUES (?, ?, ?, ?, ?, ?)
    """, rows)

    connection.commit()
    connection.close()

    print(f"Loaded {len(rows)} transactions into {DATABASE_PATH}.")


if __name__ == "__main__":
    main()
