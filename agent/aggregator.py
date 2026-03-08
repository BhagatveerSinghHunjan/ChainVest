from blockchain.logger import log_to_chain


def aggregate_results(state):

    # Log start
    

    financial = state["financial_result"]
    unit = state["unit_result"]

    # ---- Financial Scoring ----
    growth_score = max(min(financial["avg_mom_growth"], 1), 0)
    runway_score = min(financial["runway_months"] / 24, 1)
    volatility_score = 1 / (1 + financial["revenue_volatility"])

    financial_score = (growth_score + runway_score + volatility_score) / 3

    # ---- Unit Economics Scoring ----
    unit_score = unit["sustainability_score"] / 100

    # ---- Final Weighted Score ----
    final_score = (0.6 * financial_score) + (0.4 * unit_score)

    if final_score > 0.75:
        decision = "APPROVE"
    elif final_score > 0.5:
        decision = "REVIEW"
    else:
        decision = "REJECT"

    state["final_score"] = round(final_score, 3)
    state["decision"] = decision

    # Expose detailed risk scores for both the LLM node and the frontend
    state["risk_scores"] = {
        "growth_score": round(growth_score, 3),
        "runway_score": round(runway_score, 3),
        "volatility_score": round(volatility_score, 3),
        "financial_score": round(financial_score, 3),
        "unit_score": round(unit_score, 3),
        "overall_score": round(final_score, 3),
    }
    state["terminated"] = True

    return state