import sqlite3
from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data/transactions.db"

QUERY = """
    SELECT transaction_id, category, country, amount
    FROM transactions
"""


def main() -> None:
    if not DATABASE_PATH.is_file():
        raise FileNotFoundError("Run src/load_to_sqlite.py first.")

    connection = sqlite3.connect(DATABASE_PATH)
    try:
        data = pd.read_sql_query(QUERY, connection)
    finally:
        connection.close()

    features = data[["amount"]]

    model = IsolationForest(
        n_estimators=100,
        contamination="auto",
        random_state=42,
    )

    data["prediction"] = model.fit_predict(features)
    data["anomaly_score"] = model.decision_function(features)

    anomalies = data[data["prediction"] == -1]
    anomalies = anomalies.sort_values("anomaly_score")

    print("Transactions flagged by Isolation Forest:")
    print(
        anomalies[
            ["transaction_id", "category", "amount", "anomaly_score"]
        ].to_string(index=False)
    )

    print(f"\nFound {len(anomalies)} ML anomalies.")


if __name__ == "__main__":
    main()
