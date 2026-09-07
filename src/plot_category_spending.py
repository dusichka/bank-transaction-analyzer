import sqlite3
from pathlib import Path

import pandas as pd
import matplotlib

matplotlib.use("Agg")  # Save images without opening a GUI window.
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data/transactions.db"
OUTPUT_PATH = PROJECT_ROOT / "outputs/category_spending.png"

QUERY = """
    SELECT category, SUM(amount) AS total_amount
    FROM transactions
    GROUP BY category
    ORDER BY total_amount DESC
"""


def main() -> None:
    if not DATABASE_PATH.is_file():
        raise FileNotFoundError("Run src/load_to_sqlite.py first.")

    connection = sqlite3.connect(DATABASE_PATH)
    try:
        data = pd.read_sql_query(QUERY, connection)
    finally:
        connection.close()

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.bar(data["category"], data["total_amount"], color="steelblue")
    ax.set_title("Total spending by category — synthetic data")
    ax.set_xlabel("Category")
    ax.set_ylabel("Total amount")
    ax.set_ylim(bottom=0)

    fig.tight_layout()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=150)
    plt.close(fig)

    print(f"Saved chart to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
