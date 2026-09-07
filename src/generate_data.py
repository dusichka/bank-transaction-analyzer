"""Generate a small synthetic transaction dataset for the project."""

import csv
from datetime import datetime, timedelta
from pathlib import Path
from random import Random

RNG = Random(42)
OUTPUT_PATH = Path("data/raw/transactions.csv")
START_DATE = datetime(2026, 1, 1)

CATEGORIES = ["Groceries", "Transport", "Restaurants", "Electronics", "Travel"]
MERCHANTS = ["Fresh Market", "City Taxi", "Quick Bite", "Tech Store", "Sky Travel"]
COUNTRIES = ["Bulgaria", "Spain", "Germany", "Italy", "France"]


def create_transaction(transaction_number: int) -> dict[str, str | float]:
    """Create one transaction. Some transactions are deliberately unusual."""
    category_index = RNG.randrange(len(CATEGORIES))
    is_unusual = RNG.randrange(20) == 0

    if is_unusual:
        amount = round(RNG.uniform(800, 2500), 2)
    else:
        amount = round(RNG.uniform(5, 180), 2)

    timestamp = START_DATE + timedelta(
        days=RNG.randrange(90),
        minutes=RNG.randrange(24 * 60),
    )

    return {
        "transaction_id": f"TX{transaction_number:04d}",
        "timestamp": timestamp.isoformat(sep=" ", timespec="minutes"),
        "category": CATEGORIES[category_index],
        "merchant": MERCHANTS[category_index],
        "country": RNG.choice(COUNTRIES),
        "amount": amount,
    }


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "transaction_id",
                "timestamp",
                "category",
                "merchant",
                "country",
                "amount",
            ],
        )
        writer.writeheader()

        for transaction_number in range(1, 501):
            writer.writerow(create_transaction(transaction_number))

    print(f"Created {OUTPUT_PATH} with 500 transactions.")


if __name__ == "__main__":
    main()
