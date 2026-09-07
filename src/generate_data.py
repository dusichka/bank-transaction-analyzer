"""Generate a small synthetic transaction dataset for the project."""

import csv
from datetime import datetime, timedelta
from pathlib import Path
from random import Random

import argparse

PROJECT_ROOT = Path(__file__).resolve().parent.parent
START_DATE = datetime(2026, 1, 1)

CATEGORIES = ["Groceries", "Transport", "Restaurants", "Electronics", "Travel"]
MERCHANTS = ["Fresh Market", "City Taxi", "Quick Bite", "Tech Store", "Sky Travel"]
COUNTRIES = ["Bulgaria", "Spain", "Germany", "Italy", "France"]


def create_transaction(transaction_number: int, rng: Random,) -> dict[str, str | float | int]:
    """Create one transaction. Some transactions are deliberately unusual."""
    category_index = rng.randrange(len(CATEGORIES))
    is_unusual = rng.randrange(20) == 0

    if is_unusual:
        amount = round(rng.uniform(800, 2500), 2)
    else:
        amount = round(rng.uniform(5, 180), 2)

    timestamp = START_DATE + timedelta(
        days=rng.randrange(90),
        minutes=rng.randrange(24 * 60),
    )

    return {
        "transaction_id": f"TX{transaction_number:04d}",
        "timestamp": timestamp.isoformat(sep=" ", timespec="minutes"),
        "category": CATEGORIES[category_index],
        "merchant": MERCHANTS[category_index],
        "country": rng.choice(COUNTRIES),
        "amount": amount,
        "is_anomaly": int(is_unusual),
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="data/raw/transactions.csv")
    args = parser.parse_args()

    rng = Random(args.seed)
    output_path = PROJECT_ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "transaction_id",
                "timestamp",
                "category",
                "merchant",
                "country",
                "amount",
                "is_anomaly",
            ],
        )
        writer.writeheader()

        for transaction_number in range(1, 501):
            writer.writerow(create_transaction(transaction_number, rng))

    print(f"Created {output_path} with 500 transactions.")



if __name__ == "__main__":
    main()
