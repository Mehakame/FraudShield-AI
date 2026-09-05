import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "fraud_model.pkl"
)


# Load model
model = joblib.load(MODEL_PATH)


# ------------------------------------
# Suspicious transaction
# ------------------------------------

transaction = pd.DataFrame([{

    "amount": 500,

    "new_payee":0,

    "on_call": 0,

    "typing_pause": 0.5,

    "typing_variance": 0.15,

    "device_movement": 0.12,

    "transaction_hour": 15,

    "previous_transactions": 45

}])


# Prediction
prediction = model.predict(
    transaction
)[0]


# Probability
probability = model.predict_proba(
    transaction
)[0]


fraud_probability = probability[1] * 100


print("\n----- FRAUDSHIELD AI -----")

print(
    "Fraud Probability:",
    round(fraud_probability, 2),
    "%"
)


if prediction == 1:

    print(
        "Prediction: HIGH RISK 🚨"
    )

else:

    print(
        "Prediction: NORMAL ✅"
    )