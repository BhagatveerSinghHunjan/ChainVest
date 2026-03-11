import json
import os
from typing import Dict

from blockchain.logger import log_to_chain

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_KEY:
    from openai import OpenAI

    client = OpenAI()


def _mock_explanation() -> Dict:
    return {
        "market_risk_score": 70,
        "founder_risk_score": 65,
        "summary": "Moderate risk startup with stable financial indicators.",
        "strengths": [
            "Consistent revenue growth",
            "Healthy burn control",
        ],
        "weaknesses": [
            "Limited market expansion",
            "Moderate unit economics risk",
        ],
        "final_explanation": "Overall the startup shows stable metrics but moderate execution risk.",
    }


def _strip_code_fence(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```") and cleaned.endswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
        cleaned = cleaned.rsplit("```", 1)[0]
    return cleaned.strip()


def llm_reasoning_node(state):
    if not OPENAI_KEY:
        mock_output = _mock_explanation()
        state["llm_explanation"] = mock_output
        state["market_risk"] = mock_output["market_risk_score"]
        state["founder_risk"] = mock_output["founder_risk_score"]
        state = log_to_chain(state, "Mock LLM Reasoning Used", output_data=mock_output)
        return state

    risk_scores = state.get("risk_scores") or {}
    prompt = f"""
You are CEREBRUM - an explainable financial reasoning engine.

You DO NOT calculate numbers.
You ONLY interpret results using the scoring system below.

SCORING SYSTEM:

Growth Score = max(0, min(1, Avg MoM Growth))
Runway Score = min(1, Runway Months / 24)
Volatility Score = 1 / (1 + Revenue Volatility)

Financial Score = (Growth + Runway + Volatility) / 3
Unit Score = Sustainability Score / 100

Final Score = 0.6(Financial Score) + 0.4(Unit Score)

DECISION RULES:

* Final Score > 0.75 -> APPROVE
* 0.5-0.75 -> REVIEW
* <0.5 -> REJECT

YOUR TASK:

Explain the decision clearly using the given scores.

Return STRICT JSON:

{{
"market_risk_score": int (0-100),
"founder_risk_score": int (0-100),
"summary": "...",
"strengths": ["..."],
"weaknesses": ["..."],
"final_explanation": "..."
}}

DATA:
Financial Score: {risk_scores.get("financial_score")}
Unit Score: {risk_scores.get("unit_score")}
Growth Score: {risk_scores.get("growth_score")}
Runway Score: {risk_scores.get("runway_score")}
Volatility Score: {risk_scores.get("volatility_score")}
Final Score: {risk_scores.get("overall_score")}
Decision: {state.get("decision")}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )
        output_text = response.choices[0].message.content or "{}"
        parsed = json.loads(_strip_code_fence(output_text))
    except Exception as exc:
        parsed = _mock_explanation()
        parsed["fallback_reason"] = str(exc)

    state["llm_explanation"] = parsed
    return state
