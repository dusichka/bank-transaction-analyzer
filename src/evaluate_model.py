import sqlite3
from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data/transactions.db"
TEST_PATH = PROJECT_ROOT / "data/raw/test_transactions.csv"


def main() -> None:
    if not DATABASE_PATH.is_file():
        raise FileNotFoundError("Training database is missing.")

    connection = sqlite3.connect(DATABASE_PATH)
    try:
        training_data = pd.read_sql_query(
            "SELECT amount FROM transactions ORDER BY transaction_id",
            connection,
        )
    finally:
        connection.close()

    test_data = pd.read_csv(TEST_PATH)

    model = IsolationForest(
        n_estimators=100,
        contamination="auto",
        random_state=42,
    )

    model.fit(training_data[["amount"]])
    scores = model.decision_function(test_data[["amount"]])

    actual_anomalies = test_data["is_anomaly"] == 1

    print(f"Test transactions: {len(test_data)}")
    print(f"Actual synthetic anomalies: {actual_anomalies.sum()}")

    for threshold in [0.0, -0.15]:
        predicted_anomalies = scores < threshold

        true_positives = int(
            (predicted_anomalies & actual_anomalies).sum()
        )
        false_positives = int(
            (predicted_anomalies & ~actual_anomalies).sum()
        )
        false_negatives = int(
            (~predicted_anomalies & actual_anomalies).sum()
        )

        flagged_count = true_positives + false_positives
        actual_count = true_positives + false_negatives

        precision = (
            true_positives / flagged_count if flagged_count else 0.0
        )
        recall = (
            true_positives / actual_count if actual_count else 0.0
        )

        print(f"\nThreshold: {threshold}")
        print(f"Correct detections: {true_positives}")
        print(f"False alarms: {false_positives}")
        print(f"Missed anomalies: {false_negatives}")
        print(f"Precision: {precision:.1%}")
        print(f"Recall: {recall:.1%}")


if __name__ == "__main__":
    main()
