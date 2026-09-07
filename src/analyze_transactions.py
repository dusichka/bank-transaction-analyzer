import sqlite3
from pathlib import Path

DATABASE_PATH = Path("data/transactions.db")

QUERY = """
    SELECT
        category,
        COUNT(*) AS transaction_count,
        ROUND(SUM(amount), 2) AS total_amount,
        ROUND(AVG(amount), 2) AS average_amount
    FROM transactions
    GROUP BY category
    ORDER BY total_amount DESC
"""


def main() -> None:
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(QUERY)
    rows = cursor.fetchall()

    print(f"{'Category':<15} {'Transactions':>12} {'Total':>12} {'Average':>12}")
    print("-" * 55)

    for category, count, total, average in rows:
        print(f"{category:<15} {count:>12} {total:>12.2f} {average:>12.2f}")

    connection.close()


if __name__ == "__main__":
    main()
