import sqlite3
from pathlib import Path

DATABASE_PATH = Path("data/transactions.db")
THRESHOLD = 800

QUERY = """
    SELECT
        transaction_id,
        timestamp,
        category,
        merchant,
        country,
        amount
    FROM transactions
    WHERE amount > ?
    ORDER BY amount DESC
"""


def main() -> None:
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(QUERY, (THRESHOLD,))
    suspicious_transactions = cursor.fetchall()

    print(f"Suspicious transactions above {THRESHOLD}:")
    print("-" * 80)

    for transaction in suspicious_transactions:
        transaction_id, timestamp, category, merchant, country, amount = transaction

        print(
            f"{transaction_id} | {timestamp} | {category} | "
            f"{country} | {amount:.2f}"
        )

    print(f"\nFound {len(suspicious_transactions)} suspicious transactions.") 
    connection.close()


if __name__ == "__main__":
    main()
