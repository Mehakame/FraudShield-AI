import os

import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)


# =====================================================
# PROJECT PATHS
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "transactions.csv"
)


MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "fraud_model.pkl"
)


CONFUSION_MATRIX_PATH = os.path.join(
    BASE_DIR,
    "models",
    "confusion_matrix.png"
)


RESULT_FILE_PATH = os.path.join(
    BASE_DIR,
    "models",
    "evaluation_results.txt"
)


# =====================================================
# FEATURES
# =====================================================

FEATURES = [

    "amount",

    "new_payee",

    "on_call",

    "typing_pause",

    "typing_variance",

    "device_movement",

    "transaction_hour",

    "previous_transactions"
]


TARGET = "fraud"


# =====================================================
# LOAD DATASET
# =====================================================

print("\nLoading FraudShield dataset...")


data = pd.read_csv(
    DATASET_PATH
)


print(
    f"Dataset loaded successfully: {len(data)} transactions"
)


# =====================================================
# PREPARE FEATURES
# =====================================================

X = data[FEATURES]

y = data[TARGET]


# =====================================================
# SAME 80/20 TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


print(
    f"Training samples: {len(X_train)}"
)

print(
    f"Testing samples: {len(X_test)}"
)


# =====================================================
# LOAD TRAINED MODEL
# =====================================================

print("\nLoading trained Random Forest model...")


model = joblib.load(
    MODEL_PATH
)


print(
    "Model loaded successfully!"
)


# =====================================================
# PREDICTIONS
# =====================================================

predictions = model.predict(
    X_test
)


probabilities = model.predict_proba(
    X_test
)[:, 1]


# =====================================================
# METRICS
# =====================================================

accuracy = accuracy_score(
    y_test,
    predictions
)


precision = precision_score(
    y_test,
    predictions,
    zero_division=0
)


recall = recall_score(
    y_test,
    predictions,
    zero_division=0
)


f1 = f1_score(
    y_test,
    predictions,
    zero_division=0
)


roc_auc = roc_auc_score(
    y_test,
    probabilities
)


matrix = confusion_matrix(
    y_test,
    predictions
)


report = classification_report(
    y_test,
    predictions,
    target_names=[
        "Normal",
        "Fraud"
    ],
    zero_division=0
)


# =====================================================
# PRINT RESULTS
# =====================================================

print(
    "\n========================================"
)

print(
    "       FRAUDSHIELD ML EVALUATION"
)

print(
    "========================================"
)


print(
    f"\nAccuracy  : {accuracy * 100:.2f}%"
)

print(
    f"Precision : {precision * 100:.2f}%"
)

print(
    f"Recall    : {recall * 100:.2f}%"
)

print(
    f"F1 Score  : {f1 * 100:.2f}%"
)

print(
    f"ROC-AUC   : {roc_auc * 100:.2f}%"
)


print(
    "\nConfusion Matrix:"
)

print(
    matrix
)


print(
    "\nClassification Report:"
)

print(
    report
)


# =====================================================
# SAVE RESULTS
# =====================================================

with open(
    RESULT_FILE_PATH,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "FRAUDSHIELD AI - MODEL EVALUATION\n"
    )

    file.write(
        "=================================\n\n"
    )


    file.write(
        f"Accuracy  : {accuracy * 100:.2f}%\n"
    )

    file.write(
        f"Precision : {precision * 100:.2f}%\n"
    )

    file.write(
        f"Recall    : {recall * 100:.2f}%\n"
    )

    file.write(
        f"F1 Score  : {f1 * 100:.2f}%\n"
    )

    file.write(
        f"ROC-AUC   : {roc_auc * 100:.2f}%\n\n"
    )


    file.write(
        "Confusion Matrix:\n"
    )

    file.write(
        str(matrix)
    )

    file.write(
        "\n\nClassification Report:\n"
    )

    file.write(
        report
    )


print(
    f"\nEvaluation report saved at:\n{RESULT_FILE_PATH}"
)


# =====================================================
# CONFUSION MATRIX IMAGE
# =====================================================

display = ConfusionMatrixDisplay(

    confusion_matrix=matrix,

    display_labels=[
        "Normal",
        "Fraud"
    ]
)


display.plot(
    values_format="d"
)


plt.title(
    "FraudShield AI - Confusion Matrix"
)


plt.tight_layout()


plt.savefig(
    CONFUSION_MATRIX_PATH,
    dpi=300
)


print(
    f"\nConfusion matrix image saved at:\n{CONFUSION_MATRIX_PATH}"
)


plt.show()