from blockchain.logger import log_to_chain


def aggregate_results(state):

    # Log start
    

    financial = state["financial_result"]
    unit = state["unit_result"]

    # ---- Financial Scoring ----
    growth_score = max(min(financial["avg_mom_growth"], 1), 0)
    runway_score = min(financial["runway_months"] / 18, 1)
    volatility_score = 1 / (1 + financial["revenue_volatility"])

    # Base financial score (raw, un-normalized)
    financial_score_raw = (growth_score + runway_score + volatility_score) / 3

    # Normalize financial score into 0–1 based on expected range
    # so the frontend always sees values between 0 and 1.
    financial_score = max(min(financial_score_raw / 0.667, 1), 0)

    # ---- Unit Economics Scoring ----
    unit_score = unit["sustainability_score"] / 100

    # ---- Final Weighted Score ----
    # Base final score (raw, un-normalized)
    final_score_raw = (0.6 * financial_score_raw) + (0.4 * unit_score)

    # Normalize final score into 0–1 (rough cap ~0.74 in current setup)
    final_score = max(min(final_score_raw / 0.74, 1), 0)

    # Decision bands on normalized 0–1 scale
    if final_score >= 0.75:
        decision = "APPROVE"
    elif final_score >= 0.5:
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