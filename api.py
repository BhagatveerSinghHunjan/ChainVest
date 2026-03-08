from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

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


class FinancialResult(BaseModel):
    avg_mom_growth: float
    avg_burn_growth: float
    revenue_volatility: float
    runway_months: float


class UnitResult(BaseModel):
    ltv_cac_ratio: float
    payback_period_months: float
    contribution_margin: float
    sustainability_score: int


class RiskScores(BaseModel):
    growth_score: float
    runway_score: float
    volatility_score: float
    financial_score: float
    unit_score: float
    overall_score: float


class LLMExplanation(BaseModel):
    market_risk_score: int
    founder_risk_score: int
    summary: str
    strengths: List[str]
    weaknesses: List[str]
    final_explanation: str


class AnalysisResponse(BaseModel):
    mode: str
    decision: str
    final_score: float
    reasons: List[str]
    financial_result: FinancialResult
    unit_result: UnitResult
    risk_scores: Optional[RiskScores] = None
    llm_explanation: Optional[LLMExplanation] = None
    logs: List[str]
    tx_hashes: List[str]

@app.post("/analyze", response_model=AnalysisResponse)
def analyze(data: InputSchema) -> AnalysisResponse:

    print("\n===== NEW REQUEST =====")

    result = run_agent(
        data.mode,
        [data.revenue]*12,
        [data.burn]*12,
        data.cash
    )

    print("RESULT:", result)

    return result   # ✅ THIS LINE FIXES EVERYTHING