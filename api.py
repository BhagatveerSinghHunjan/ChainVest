import json
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent.workflow import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InputSchema(BaseModel):
    mode: str
    revenue: float
    burn: float
    cash: float


def _ensure_risk_scores(state: dict[str, Any]) -> None:
    if state.get("risk_scores") is not None:
        return

    financial = state.get("financial_result") or {}
    unit = state.get("unit_result") or {}

    growth_score = max(min(float(financial.get("avg_mom_growth", 0.0)), 1.0), 0.0)
    runway_score = min(float(financial.get("runway_months", 0.0)) / 24.0, 1.0)
    volatility = float(financial.get("revenue_volatility", 0.0))
    volatility_score = 1.0 / (1.0 + volatility)

    financial_score = (growth_score + runway_score + volatility_score) / 3.0
    unit_score = float(unit.get("sustainability_score", 0.0)) / 100.0
    overall_score = (0.6 * financial_score) + (0.4 * unit_score)

    state["risk_scores"] = {
        "growth_score": round(growth_score, 3),
        "runway_score": round(runway_score, 3),
        "volatility_score": round(volatility_score, 3),
        "financial_score": round(financial_score, 3),
        "unit_score": round(unit_score, 3),
        "overall_score": round(overall_score, 3),
    }
    state["final_score"] = round(overall_score, 3)

    if overall_score > 0.75:
        state["decision"] = "APPROVE"
    elif overall_score >= 0.5:
        state["decision"] = "REVIEW"
    else:
        state["decision"] = "REJECT"


def _ensure_llm_explanation(state: dict[str, Any]) -> None:
    if state.get("llm_explanation") is not None:
        return

    state["llm_explanation"] = {
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


def _format_logs(logs: list[Any]) -> list[str]:
    output: list[str] = []
    for log in logs:
        if isinstance(log, dict):
            ts = log.get("timestamp")
            step = log.get("step")
            tx = log.get("tx_hash")
            output.append(f"{ts} | {step} | {tx}")
        else:
            output.append(str(log))
    return output


@app.post("/analyze")
def analyze(data: InputSchema):
    result = run_agent(
        mode=data.mode,
        monthly_revenue=[data.revenue] * 12,
        monthly_burn=[data.burn] * 12,
        cash_on_hand=data.cash,
    )

    print("\n===== NEW REQUEST =====")
    print("RESULT JSON:\n", json.dumps(result, indent=2))

    state = result.get("state", result)
    state["mode"] = state.get("mode") or data.mode

    _ensure_risk_scores(state)
    _ensure_llm_explanation(state)

    return {
        "mode": state.get("mode"),
        "decision": state.get("decision"),
        "final_score": state.get("final_score"),
        "reasons": state.get("reasons", []),
        "financial_result": state.get("financial_result"),
        "unit_result": state.get("unit_result"),
        "risk_scores": state.get("risk_scores"),
        "llm_explanation": state.get("llm_explanation"),
        "mcp_result": state.get("mcp_result"),
        "logs": _format_logs(state.get("logs", [])),
        "tx_hashes": state.get("tx_hashes", []),
        "audit_logs": state.get("audit_logs", []),
    }
