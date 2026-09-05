import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ------------------------------------
# 1. Find project paths
# ------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "transactions.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "fraud_model.pkl"
)


# ------------------------------------
# 2. Load dataset
# ------------------------------------

df = pd.read_csv(DATA_PATH)

print("\nDataset loaded successfully!")
print("Total records:", len(df))


# ------------------------------------
# 3. Select features
# ------------------------------------

features = [
    "amount",
    "new_payee",
    "on_call",
    "typing_pause",
    "typing_variance",
    "device_movement",
    "transaction_hour",
    "previous_transactions"
]

X = df[features]

y = df["fraud"]


# ------------------------------------
# 4. Split dataset
# ------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))


# ------------------------------------
# 5. Create Random Forest model
# ------------------------------------

model = RandomForestClassifier(
    n_estimators=150,
    random_state=42,
    class_weight="balanced"
)


# ------------------------------------
# 6. Train model
# ------------------------------------

print("\nTraining model...")

model.fit(
    X_train,
    y_train
)

print("Training completed!")


# ------------------------------------
# 7. Predictions
# ------------------------------------

y_pred = model.predict(X_test)


# ------------------------------------
# 8. Accuracy
# ------------------------------------

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n----- MODEL RESULTS -----")

print(
    "Accuracy:",
    round(accuracy * 100, 2),
    "%"
)


# ------------------------------------
# 9. Classification report
# ------------------------------------

print("\n----- CLASSIFICATION REPORT -----")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Normal",
            "Fraud"
        ],
        zero_division=0
    )
)


# ------------------------------------
# 10. Confusion Matrix
# ------------------------------------

print("\n----- CONFUSION MATRIX -----")

cm = confusion_matrix(
    y_test,
    y_pred
)

print(cm)


# ------------------------------------
# 11. Feature Importance
# ------------------------------------

print("\n----- FEATURE IMPORTANCE -----")

importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)

print(importance)


# ------------------------------------
# 12. Save model
# ------------------------------------

joblib.dump(
    model,
    MODEL_PATH
)

print(
    "\nModel saved successfully:"
)

print(MODEL_PATH)