import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sqlite3
from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data/transactions.db"
OUTPUT_PATH = PROJECT_ROOT / "outputs/ml_anomaly_scores.png"
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

    normal = data[data["prediction"] == 1]
    flagged = data[data["prediction"] == -1]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(normal["amount"], normal["anomaly_score"], color="steelblue", label="Not flagged", alpha=0.6, s=25,)
    ax.scatter(
        flagged["amount"],
        flagged["anomaly_score"],
        color="crimson",
        label="Flagged by model",
        alpha=0.8,
        s=30,
    )

    ax.axhline(
        y=0,
        color="black",
        linestyle="--",
        label="Default threshold",
    )

    ax.set_title("Isolation Forest scores — synthetic transactions")
    ax.set_xlabel("Transaction amount")
    ax.set_ylabel("Anomaly score (lower = more unusual)")
    ax.legend()
    ax.grid(alpha=0.2)

    fig.tight_layout()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=150)
    plt.close(fig)

    print(f"Saved chart to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
