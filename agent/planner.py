def decide_next_step(state):
    if state["financial_result"] is None:
        return "financial"

    if state["unit_result"] is None:
        return "unit"

    return "aggregate"