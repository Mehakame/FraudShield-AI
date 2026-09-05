import pandas as pd
import numpy as np
import random

# Reproducible dataset
np.random.seed(42)
random.seed(42)

data = []

TOTAL_RECORDS = 3000

for i in range(TOTAL_RECORDS):

    # -----------------------------
    # Basic transaction information
    # -----------------------------
    amount = round(np.random.uniform(100, 50000), 2)

    new_payee = np.random.choice(
        [0, 1],
        p=[0.7, 0.3]
    )

    on_call = np.random.choice(
        [0, 1],
        p=[0.8, 0.2]
    )

    typing_pause = round(
        np.random.uniform(0.1, 10),
        2
    )

    typing_variance = round(
        np.random.uniform(0.05, 1),
        2
    )

    device_movement = round(
        np.random.uniform(0.05, 1),
        2
    )

    transaction_hour = np.random.randint(0, 24)

    previous_transactions = np.random.randint(0, 100)

    # -----------------------------
    # Hidden fraud scoring logic
    # Only used to generate labels
    # -----------------------------
    fraud_score = 0

    if amount >= 20000:
        fraud_score += 2

    if new_payee == 1:
        fraud_score += 2

    if on_call == 1:
        fraud_score += 2

    if typing_pause >= 5:
        fraud_score += 2

    if typing_variance >= 0.7:
        fraud_score += 1

    if device_movement >= 0.7:
        fraud_score += 1

    # Late-night transactions
    if transaction_hour <= 4:
        fraud_score += 1

    # New / rarely used account
    if previous_transactions <= 3:
        fraud_score += 1

    # -----------------------------
    # Assign fraud label
    # -----------------------------
    if fraud_score >= 6:
        fraud = 1
    else:
        fraud = 0

    # Add small randomness so data
    # isn't perfectly rule-based
    if random.random() < 0.03:
        fraud = 1 - fraud

    data.append({
        "amount": amount,
        "new_payee": new_payee,
        "on_call": on_call,
        "typing_pause": typing_pause,
        "typing_variance": typing_variance,
        "device_movement": device_movement,
        "transaction_hour": transaction_hour,
        "previous_transactions": previous_transactions,
        "fraud": fraud
    })


df = pd.DataFrame(data)

df.to_csv(
    "transactions.csv",
    index=False
)

print("\nDataset created successfully!")
print("Total records:", len(df))

print("\nFraud distribution:")
print(df["fraud"].value_counts())

print("\nFraud percentage:")
print(
    round(df["fraud"].mean() * 100, 2),
    "%"
)

print("\nFirst 5 rows:")
print(df.head())