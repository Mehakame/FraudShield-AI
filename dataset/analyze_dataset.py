import pandas as pd

df = pd.read_csv("transactions.csv")

print("\n----- DATASET INFORMATION -----")
print(df.info())

print("\n----- FIRST 5 RECORDS -----")
print(df.head())

print("\n----- MISSING VALUES -----")
print(df.isnull().sum())

print("\n----- FRAUD DISTRIBUTION -----")
print(df["fraud"].value_counts())

print("\n----- FRAUD PERCENTAGE -----")

fraud_percentage = (
    df["fraud"].mean() * 100
)

print(
    round(fraud_percentage, 2),
    "%"
)

print("\n----- AVERAGE TRANSACTION AMOUNT -----")

print(
    round(df["amount"].mean(), 2)
)

print("\n----- FRAUD TRANSACTIONS SAMPLE -----")

fraud_transactions = df[
    df["fraud"] == 1
]

print(
    fraud_transactions.head(10)
)