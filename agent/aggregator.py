def aggregate_results(state):
    financial = state["financial_result"]
    unit = state["unit_result"]

    # ---- Financial Scoring ----
    # Normalize growth between 0 and 1
    growth_score = max(min(financial["avg_mom_growth"], 1), 0)

    # Runway normalization (24 months ideal)
    runway_score = min(financial["runway_months"] / 24, 1)

    # Lower volatility is better
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

    return state