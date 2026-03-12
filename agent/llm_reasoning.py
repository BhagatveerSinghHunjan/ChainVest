import json
import os

from blockchain.logger import log_to_chain
from dotenv import load_dotenv

load_dotenv()

CEREBRUM_BASE_URL = os.getenv("CEREBRUM_BASE_URL") or os.getenv("OPENAI_BASE_URL")
CEREBRUM_MODEL = os.getenv("CEREBRUM_MODEL") or os.getenv("OPENAI_MODEL") or "gpt-4o-mini"
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
LLM_ENABLED = bool(OPENAI_KEY or CEREBRUM_BASE_URL)

if LLM_ENABLED:
    from openai import OpenAI

    client = OpenAI(
        api_key=OPENAI_KEY or "dummy",
        base_url=CEREBRUM_BASE_URL,
    )


def _strip_code_fence(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```") and cleaned.endswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
        cleaned = cleaned.rsplit("```", 1)[0]
    return cleaned.strip()


def llm_reasoning_node(state):
    if not LLM_ENABLED:
        state["llm_trace"] = {
            "provider": "disabled",
            "model": None,
            "prompt": None,
            "raw_response": None,
            "reason": "Cerebrum client is not configured",
        }
        state["llm_explanation"] = None
        state = log_to_chain(
            state,
            "LLM Reasoning Skipped",
            output_data={"reason": "Cerebrum client is not configured"},
        )
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
Business Score = Business Assessment Score / 100

Final Score = 0.45(Financial Score) + 0.25(Unit Score) + 0.30(Business Score)

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
Business Description: {state.get("startup_data", {}).get("business_description") or "N/A"}
Financial Score: {risk_scores.get("financial_score")}
Unit Score: {risk_scores.get("unit_score")}
Business Score: {risk_scores.get("business_score")}
Business Assessment: {state.get("business_result")}
Growth Score: {risk_scores.get("growth_score")}
Runway Score: {risk_scores.get("runway_score")}
Volatility Score: {risk_scores.get("volatility_score")}
Final Score: {risk_scores.get("overall_score")}
Decision: {state.get("decision")}
"""

    try:
        response = client.chat.completions.create(
            model=CEREBRUM_MODEL,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )
        output_text = response.choices[0].message.content or "{}"
        parsed = json.loads(_strip_code_fence(output_text))
        state["llm_trace"] = {
            "provider": "cerebrum" if CEREBRUM_BASE_URL else "openai-compatible",
            "model": CEREBRUM_MODEL,
            "prompt": prompt,
            "raw_response": output_text,
        }
    except Exception as exc:
        parsed = None
        state["llm_trace"] = {
            "provider": "error",
            "model": None,
            "prompt": prompt,
            "raw_response": None,
            "error": str(exc),
        }

    state["llm_explanation"] = parsed
    return state
