def create_transaction(
    sender,
    receiver,
    amount,
    new_payee,
    on_call,
    typing_pause,
    typing_variance,
    device_movement
):
    transaction = {
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "new_payee": new_payee,
        "on_call": on_call,
        "typing_pause": typing_pause,
        "typing_variance": typing_variance,
        "device_movement": device_movement
    }

    return transaction