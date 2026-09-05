import requests
import json


API_URL = "http://127.0.0.1:8000/predict"


# =====================================================
# TEST FUNCTION
# =====================================================

def run_test(
    test_name,
    receiver,
    amount,
    new_payee,
    on_call,
    typing_pause,
    typing_variance,
    device_movement,
    expected_description
):

    request_data = {

        "sender": "TESTUSER001",

        "receiver": receiver,

        "amount": amount,

        "new_payee": new_payee,

        "on_call": on_call,

        "typing_pause": typing_pause,

        "typing_variance": typing_variance,

        "device_movement": device_movement,

        "transaction_hour": 14,

        "previous_transactions": 5
    }


    print(
        "\n========================================"
    )

    print(
        test_name
    )

    print(
        "========================================"
    )


    print(
        "Expected:",
        expected_description
    )


    try:

        response = requests.post(

            API_URL,

            json=request_data,

            timeout=15
        )


        response.raise_for_status()


        result = response.json()


        print(
            "\nReceiver:",
            receiver
        )


        print(
            "Behavior Risk:",
            result.get(
                "behavioral_risk_level"
            )
        )


        print(
            "Behavior Score:",
            result.get(
                "fraud_probability"
            )
        )


        print(
            "Graph Risk:",
            result.get(
                "graph_risk_level"
            )
        )


        print(
            "Graph Score:",
            result.get(
                "graph_risk_score"
            )
        )


        print(
            "Final Risk:",
            result.get(
                "risk_level"
            )
        )


        print(
            "Action:",
            result.get(
                "action"
            )
        )


        print(
            "\nRisk Signals:"
        )


        signals = result.get(
            "risk_signals",
            []
        )


        if signals:

            for signal in signals:

                print(
                    "•",
                    signal
                )

        else:

            print(
                "No major risk signals"
            )


    except requests.RequestException as error:

        print(
            "\nTEST FAILED:"
        )

        print(
            error
        )


# =====================================================
# TEST 1
# NORMAL USER + NORMAL RECEIVER
# =====================================================

run_test(

    test_name=
        "TEST 1 - Normal Behavior + Normal Receiver",

    receiver=
        "SAFE9001",

    amount=
        500,

    new_payee=
        0,

    on_call=
        0,

    typing_pause=
        0.5,

    typing_variance=
        0.1,

    device_movement=
        0.1,

    expected_description=
        "Low behavioral and graph risk"
)


# =====================================================
# TEST 2
# SUSPICIOUS BEHAVIOR
# =====================================================

run_test(

    test_name=
        "TEST 2 - Suspicious Behavior + Normal Receiver",

    receiver=
        "SAFE9002",

    amount=
        25000,

    new_payee=
        1,

    on_call=
        1,

    typing_pause=
        7.5,

    typing_variance=
        0.85,

    device_movement=
        0.80,

    expected_description=
        "High behavioral risk"
)


# =====================================================
# TEST 3
# NORMAL BEHAVIOR + MULE RECEIVER
# =====================================================

run_test(

    test_name=
        "TEST 3 - Normal Behavior + Mule Receiver",

    receiver=
        "MULE100",

    amount=
        500,

    new_payee=
        1,

    on_call=
        0,

    typing_pause=
        0.5,

    typing_variance=
        0.1,

    device_movement=
        0.1,

    expected_description=
        "Low behavioral risk but HIGH graph risk"
)


# =====================================================
# TEST 4
# SUSPICIOUS BEHAVIOR + MULE
# =====================================================

run_test(

    test_name=
        "TEST 4 - Suspicious Behavior + Mule Receiver",

    receiver=
        "MULE100",

    amount=
        30000,

    new_payee=
        1,

    on_call=
        1,

    typing_pause=
        8.0,

    typing_variance=
        0.90,

    device_movement=
        0.90,

    expected_description=
        "High behavioral and graph risk"
)


print(
    "\n========================================"
)

print(
    "FraudShield system testing completed"
)

print(
    "========================================"
)