from transaction import create_transaction
from risk_engine import calculate_risk


transaction = create_transaction(
    sender="USER001",
    receiver="ACC999",
    amount=25000,
    new_payee=1,
    on_call=1,
    typing_pause=7.5,
    typing_variance=0.8,
    device_movement=0.75
)


result = calculate_risk(transaction)


print("\n----- TRANSACTION -----")

for key, value in transaction.items():
    print(f"{key}: {value}")


print("\n----- FRAUD ANALYSIS -----")

print("Risk Score:", result["risk_score"])
print("Risk Level:", result["risk_level"])

print("\nReasons:")

for reason in result["reasons"]:
    print("-", reason)