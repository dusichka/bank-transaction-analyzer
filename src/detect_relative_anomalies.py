import sqlite3
from pathlib import Path

DATABASE_PATH = Path("data/transactions.db")
MULTIPLIER = 3

QUERY = """
    SELECT
        t.transaction_id,
        t.category,
        t.country,
        t.amount,
        ROUND(averages.category_average, 2) AS category_average,
        ROUND(t.amount / averages.category_average, 2) AS ratio
    FROM transactions AS t
    JOIN (
        SELECT
            category,
            AVG(amount) AS category_average
        FROM transactions
        GROUP BY category
    ) AS averages
    ON t.category = averages.category
    WHERE t.amount > averages.category_average * ?
    ORDER BY ratio DESC
"""


def main() -> None:
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(QUERY, (MULTIPLIER,))
    suspicious_transactions = cursor.fetchall()

    print("Transactions more than 3 times their category average:")
    print("-" * 80)

    for transaction_id, category, country, amount, average, ratio in suspicious_transactions:
        print(
            f"{transaction_id} | {category:<12} | {country:<10} | "
            f"{amount:>8.2f} | average: {average:>7.2f} | {ratio}x"
        )

    print(f"\nFound {len(suspicious_transactions)} relative anomalies.")
    connection.close()


if __name__ == "__main__":
    main()
