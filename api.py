from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

from agent.workflow import run_agent

import json

app = FastAPI()

# -----------------------------
# CORS (Frontend Connection)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# INPUT SCHEMA
# -----------------------------
class InputSchema(BaseModel):
    mode: str
    revenue: float
    burn: float
    cash: float


# -----------------------------
# API ROUTE
# -----------------------------
@app.post("/analyze")
def analyze(data: InputSchema):

    print("\n===== NEW REQUEST =====")

    # -----------------------------
    # RUN AGENT (REAL EXECUTION)
    # -----------------------------
    result = run_agent(
        data.mode,
        [data.revenue] * 12,   # REQUIRED FORMAT
        [data.burn] * 12,      # REQUIRED FORMAT
        data.cash
    )

    # DEBUG (optional but useful)
    print("RESULT JSON:\n", json.dumps(result, indent=2))

    # -----------------------------
    # IMPORTANT FIX
    # run_agent sometimes nests state
    # -----------------------------
    state = result.get("state", result)

    # -----------------------------
    # FORMAT LOGS (dict → string)
    # -----------------------------
    formatted_logs = []
    for log in state.get("logs", []):
        if isinstance(log, dict):
            ts = log.get("timestamp")
            step = log.get("step")
            tx = log.get("tx_hash")
            formatted_logs.append(f"{ts} | {step} | {tx}")
        else:
            formatted_logs.append(str(log))

    # -----------------------------
    # FINAL RESPONSE (WORKS PERFECT)
    # -----------------------------
    return {
        "mode": state.get("mode"),
        "decision": state.get("decision"),
        "final_score": state.get("final_score"),
        "reasons": state.get("reasons", []),

        "financial_result": state.get("financial_result"),
        "unit_result": state.get("unit_result"),

        # ⭐ THIS FIXES YOUR N/A ISSUE
        "risk_scores": state.get("risk_scores"),

        "llm_explanation": state.get("llm_explanation"),

        "logs": formatted_logs,
        "tx_hashes": state.get("tx_hashes", []),
    }