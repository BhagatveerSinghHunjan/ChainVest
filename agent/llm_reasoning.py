import json
import os
from blockchain.logger import log_to_chain

# Only import OpenAI if key exists
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_KEY:
    from openai import OpenAI
    client = OpenAI()


def llm_reasoning_node(state):

    # STEP 1 — If no API key → use MOCK (IMPORTANT)
    if not OPENAI_KEY:

        mock_output = {
            "market_risk_score": 70,
            "founder_risk_score": 65,
            "summary": "Moderate risk startup with stable financial indicators.",
            "strengths": [
                "Consistent revenue growth",
                "Healthy burn control"
            ],
            "weaknesses": [
                "Limited market expansion",
                "Moderate unit economics risk"
            ],
            "final_explanation": "Overall the startup shows stable metrics but moderate execution risk."
        }

        state["llm_explanation"] = mock_output
        state["market_risk"] = mock_output["market_risk_score"]
        state["founder_risk"] = mock_output["founder_risk_score"]

        state = log_to_chain(
            state,
            "Mock LLM Reasoning Used",
             output_data=mock_output
        )

        return state

    # STEP 2 — REAL LLM (when key available)
    snapshot = f"""
Mode: {state.get('mode')}
Financial Score: {state['risk_scores'].get('financial_score')}
Economics Score: {state['risk_scores'].get('economics_score')}
Overall Score: {state['risk_scores'].get('overall_score')}
Decision: {state.get('decision')}
"""

    prompt = f"""
You are a financial decision explanation engine.

You DO NOT calculate numbers.
You ONLY explain given results.

Return valid JSON only:

DATA:
{snapshot}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    output_text = response.choices[0].message.content

    try:
        parsed = json.loads(output_text)
    except:
        parsed = {"final_explanation": output_text}

    state["llm_explanation"] = parsed

    state = log_to_chain(
    state,
    "Mock LLM Reasoning Used",
    output_data=mock_output
    )

    return state