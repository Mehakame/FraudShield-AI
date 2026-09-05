import os

import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel, Field

from graph_engine.neo4j_client import (
    Neo4jGraphEngine
)


# =====================================================
# FASTAPI
# =====================================================

app = FastAPI(

    title=
        "FraudShield AI API",

    description=
        "Behavioral AI + Advanced Graph Fraud Detection",

    version=
        "3.0"
)


# =====================================================
# MODEL
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


MODEL_PATH = os.path.join(

    BASE_DIR,

    "models",

    "fraud_model.pkl"
)


model = joblib.load(
    MODEL_PATH
)


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


# =====================================================
# NEO4J
# =====================================================

graph_engine = None


try:

    graph_engine =Neo4jGraphEngine()

    graph_engine.verify_connection()

    print(
        "Advanced graph engine ready!"
    )


except Exception as e:

    print(
        "Neo4j unavailable:",
        str(e)
    )


# =====================================================
# REQUEST MODEL
# =====================================================

class TransactionInput(
    BaseModel
):

    sender: str = Field(
        min_length=1
    )

    receiver: str = Field(
        min_length=1
    )

    amount: float = Field(
        gt=0
    )

    new_payee: int = Field(
        ge=0,
        le=1
    )

    on_call: int = Field(
        ge=0,
        le=1
    )

    typing_pause: float = Field(
        ge=0
    )

    typing_variance: float = Field(
        ge=0,
        le=1
    )

    device_movement: float = Field(
        ge=0,
        le=1
    )

    transaction_hour: int = Field(
        ge=0,
        le=23
    )

    previous_transactions: int = Field(
        ge=0
    )


# =====================================================
# HOME
# =====================================================

@app.get("/")
def home():

    return {

        "message":
            "FraudShield AI API running",

        "ml":
            "READY",

        "neo4j":
            (
                "READY"
                if graph_engine
                else "UNAVAILABLE"
            )
    }


# =====================================================
# PREDICT
# =====================================================

@app.post("/predict")
def predict(
    transaction: TransactionInput
):

    # =================================================
    # BEHAVIOR ML
    # =================================================

    dataframe = pd.DataFrame(
        [{

            "amount":
                transaction.amount,

            "new_payee":
                transaction.new_payee,

            "on_call":
                transaction.on_call,

            "typing_pause":
                transaction.typing_pause,

            "typing_variance":
                transaction.typing_variance,

            "device_movement":
                transaction.device_movement,

            "transaction_hour":
                transaction.transaction_hour,

            "previous_transactions":
                transaction.previous_transactions

        }]
    )


    probability = (
        model
        .predict_proba(
            dataframe
        )[0][1]
    )


    behavioral_score = round(
        float(probability) * 100,
        2
    )


    if behavioral_score >= 70:

        behavioral_level ="HIGH"

    elif behavioral_score >= 30:

        behavioral_level ="MEDIUM"

    else:

        behavioral_level ="LOW"


    # =================================================
    # BEHAVIOR REASONS
    # =================================================

    behavioral_signals = []


    if transaction.amount >= 20000:

        behavioral_signals.append(
            "High transaction amount"
        )


    if transaction.new_payee == 1:

        behavioral_signals.append(
            "New beneficiary"
        )


    if transaction.on_call == 1:

        behavioral_signals.append(
            "User currently on phone call"
        )


    if transaction.typing_pause >= 5:

        behavioral_signals.append(
            "Long typing pause"
        )


    if transaction.typing_variance >= 0.7:

        behavioral_signals.append(
            "Irregular typing behavior"
        )


    if transaction.device_movement >= 0.7:

        behavioral_signals.append(
            "Unusual device movement"
        )


    # =================================================
    # GRAPH DEFAULTS
    # =================================================

    graph_score = 0

    graph_level = "LOW"

    graph_status = "UNAVAILABLE"

    graph_reasons = []

    total_transactions = 0

    reachable_accounts = 0

    max_hop_depth = 0

    rapid_chain_count = 0

    pass_through_ratio = 0.0


    # =================================================
    # GRAPH ANALYSIS
    # =================================================

    if graph_engine is not None:

        try:

            sender = (
                transaction
                .sender
                .strip()
                .upper()
            )


            receiver = (
                transaction
                .receiver
                .strip()
                .upper()
            )


            graph_engine.add_transaction(

                sender=
                    sender,

                receiver=
                    receiver,

                amount=
                    transaction.amount
            )


            graph_result = (
                graph_engine
                .analyze_account(
                    receiver
                )
            )


            graph_score = (
                graph_result[
                    "graph_risk_score"
                ]
            )


            graph_level = (
                graph_result[
                    "graph_risk_level"
                ]
            )


            graph_reasons = (
                graph_result[
                    "reasons"
                ]
            )


            total_transactions = (
                graph_result[
                    "total_transactions"
                ]
            )


            reachable_accounts = (
                graph_result[
                    "reachable_accounts"
                ]
            )


            max_hop_depth = (
                graph_result[
                    "max_hop_depth"
                ]
            )


            rapid_chain_count = (
                graph_result[
                    "rapid_chain_count"
                ]
            )


            pass_through_ratio = (
                graph_result[
                    "pass_through_ratio"
                ]
            )


            graph_status ="READY"


        except Exception as e:

            graph_status ="ERROR"

            print(
                "Graph error:",
                str(e)
            )


    # =================================================
    # COMBINED SCORE
    # =================================================

    combined_score = round(

        max(
            behavioral_score,
            graph_score
        ),

        2
    )


    # =================================================
    # FINAL DECISION
    # =================================================

    if combined_score >= 70:

        final_level ="HIGH"

        action ="HOLD"

        prediction = "FRAUD"


    elif combined_score >= 30:

        final_level =    "MEDIUM"

        action ="WARN"

        prediction ="SUSPICIOUS"


    else:

        final_level = "LOW"

        action = "ALLOW"

        prediction ="NORMAL"


    all_signals = list(

        dict.fromkeys(

            behavioral_signals
            +
            graph_reasons
        )
    )


    # =================================================
    # RESPONSE
    # =================================================

    return {

        "prediction":
            prediction,

        "risk_level":
            final_level,

        "action":
            action,

        "combined_risk_score":
            combined_score,


        "fraud_probability":
            behavioral_score,

        "behavioral_risk_level":
            behavioral_level,


        "graph_risk_score":
            graph_score,

        "graph_risk_level":
            graph_level,

        "graph_status":
            graph_status,


        # ADVANCED GRAPH VALUES

        "total_graph_transactions":
            total_transactions,

        "reachable_accounts":
            reachable_accounts,

        "max_hop_depth":
            max_hop_depth,

        "rapid_chain_count":
            rapid_chain_count,

        "pass_through_ratio":
            pass_through_ratio,


        "graph_reasons":
            graph_reasons,

        "risk_signals":
            all_signals
    }