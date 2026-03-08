import random


def audit_step(state, step_name):

    """
    Mock Weilliptic AI Auditor
    Assigns transparency + anomaly score
    """

    # --- Transparency Score ---
    transparency_score = random.randint(85, 100)

    # --- Integrity Check ---
    anomaly_flag = False

    if step_name == "Financial Analysis Completed":
        if state["financial_result"]["runway_months"] < 3:
            anomaly_flag = True

    # --- Save inside state ---
    audit_entry = {
        "step": step_name,
        "transparency_score": transparency_score,
        "anomaly_flag": anomaly_flag
    }

    if "audit_logs" not in state:
        state["audit_logs"] = []

    state["audit_logs"].append(audit_entry)

    return state