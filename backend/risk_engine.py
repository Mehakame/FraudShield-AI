def calculate_risk(transaction):

    risk_score = 0
    reasons = []

    # -----------------------------
    # Large transaction
    # -----------------------------
    if transaction["amount"] >= 20000:
        risk_score += 25
        reasons.append("Large transaction amount")

    # -----------------------------
    # New receiver
    # -----------------------------
    if transaction["new_payee"] == 1:
        risk_score += 20
        reasons.append("Transaction to new beneficiary")

    # -----------------------------
    # User currently on call
    # -----------------------------
    if transaction["on_call"] == 1:
        risk_score += 20
        reasons.append("User may be on a phone call")

    # -----------------------------
    # Long typing pause
    # -----------------------------
    if transaction["typing_pause"] >= 5:
        risk_score += 15
        reasons.append("Abnormally long typing pause")

    # -----------------------------
    # Irregular typing
    # -----------------------------
    if transaction["typing_variance"] >= 0.7:
        risk_score += 10
        reasons.append("Unusual typing behaviour")

    # -----------------------------
    # Device movement
    # -----------------------------
    if transaction["device_movement"] >= 0.7:
        risk_score += 10
        reasons.append("Unusual device movement")

    # Risk category

    if risk_score >= 70:
        risk_level = "HIGH"

    elif risk_score >= 40:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reasons": reasons
    }