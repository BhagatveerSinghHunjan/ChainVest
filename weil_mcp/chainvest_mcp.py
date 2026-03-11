def evaluate_startup(revenue, burn, cash):

    score = (revenue / (burn + 1)) * (cash / 10000)

    if score > 5:
        decision = "APPROVE"
    elif score > 2:
        decision = "REVIEW"
    else:
        decision = "REJECT"

    return {
        "decision": decision,
        "score": round(score, 2)
    }