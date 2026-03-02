def aggregate_results(state):
    financial_score = state["financial_result"]["score"]
    unit_score = state["unit_result"]["score"]

    final_score = (financial_score + unit_score) / 2

    if final_score > 0.7:
        decision = "APPROVE"
    elif final_score > 0.4:
        decision = "REVIEW"
    else:
        decision = "REJECT"

    state["final_score"] = final_score
    state["decision"] = decision

    return state