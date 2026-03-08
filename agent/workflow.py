from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.aggregator import aggregate_results
from blockchain.logger import log_to_chain
from agent.llm_reasoning import llm_reasoning_node

from tools.financial_trends import FinancialTrendAnalyzer
from tools.unit_economics import UnitEconomicsEngine
from schemas.financial_input import FinancialInput
from schemas.economics_input import UnitEconomicsInput


# --------------------------------------------------
# Financial Analysis Node
# --------------------------------------------------
def financial_node(state: AgentState):

    state = log_to_chain(state, "Financial Analysis Started")

    analyzer = FinancialTrendAnalyzer()
    financial_input = FinancialInput(**state["startup_data"])
    result = analyzer.analyze(financial_input)

    state["financial_result"] = result

    state = log_to_chain(state, "Financial Analysis Completed")

    return state


# --------------------------------------------------
# Unit Economics Node
# --------------------------------------------------
def unit_node(state: AgentState):

    state = log_to_chain(state, "Unit Economics Analysis Started")

    engine = UnitEconomicsEngine()
    unit_input = UnitEconomicsInput(**state["startup_data"])
    result = engine.analyze(unit_input)

    state["unit_result"] = result

    state = log_to_chain(state, "Unit Economics Analysis Completed")

    return state


# --------------------------------------------------
# Final Node (NEW - Required)
# --------------------------------------------------
def final_node(state: AgentState):

    state = log_to_chain(state, "Final Decision Generated")

    state["finished"] = True
    return state


# --------------------------------------------------
# Build Graph (STAGE 4 VERSION)
# --------------------------------------------------
def build_graph():

    builder = StateGraph(AgentState)

    # ✅ Add Nodes
    builder.add_node("financial", financial_node)
    builder.add_node("unit", unit_node)
    builder.add_node("aggregate", aggregate_results)

    # ⭐ NEW Stage 4 Node
    builder.add_node("llm_reasoning", llm_reasoning_node)

    # ⭐ Final Node
    builder.add_node("finalize", final_node)

    # Entry point
    builder.set_entry_point("financial")

    # ✅ Flow (UPDATED FOR STAGE 4)
    builder.add_edge("financial", "unit")
    builder.add_edge("unit", "aggregate")

    # ⭐ Stage 4 flow
    builder.add_edge("aggregate", "llm_reasoning")
    builder.add_edge("llm_reasoning", "finalize")

    builder.add_edge("finalize", END)

    graph = builder.compile()

    # Generate workflow diagram
    graph.get_graph().draw_mermaid_png(output_file_path="workflow.png")

    return graph


# --------------------------------------------------
# Public entrypoint for the API
# --------------------------------------------------
def run_agent(
    mode: str,
    monthly_revenue: list[float],
    monthly_burn: list[float],
    cash_on_hand: float,
    ltv: float = 900,
    cac: float = 300,
    gross_margin: float = 60,
    monthly_new_customers: int = 50,
):

    # Build startup data in the same shape used by run_test.py
    startup_data = {
        "monthly_revenue": monthly_revenue,
        "monthly_burn": monthly_burn,
        "cash_on_hand": cash_on_hand,
        "ltv": ltv,
        "cac": cac,
        "gross_margin": gross_margin,
        "monthly_new_customers": monthly_new_customers,
    }

    # Initial graph state (same keys as run_test.py)
    initial_state = {
        "startup_data": startup_data,
        "financial_result": None,
        "unit_result": None,
        "final_score": None,
        "decision": None,
        "logs": [],
        "tx_hashes": [],
        "next_action": None,
        "terminated": False,
    }

    # Run the LangGraph workflow
    graph = build_graph()
    result = graph.invoke(initial_state)

    financial = result["financial_result"]
    unit = result.get("unit_result")
    decision = result["decision"]
    score = result["final_score"]

    # Build human‑readable reasons (same rules as run_test.py)
    reasons = []

    if financial["runway_months"] < 6:
        reasons.append("Cash runway is less than 6 months.")

    if financial["avg_mom_growth"] < 0.05:
        reasons.append("Revenue growth is weak.")

    if financial["revenue_volatility"] > 30:
        reasons.append("Revenue shows high volatility.")

    if not reasons:
        reasons.append("Financial performance is stable and healthy.")

    # Turn internal log dicts into readable strings for the frontend
    formatted_logs = []
    for log in result.get("logs", []):
        # each log is {"timestamp": ..., "step": ..., "tx_hash": ...}
        ts = log.get("timestamp")
        step = log.get("step")
        tx = log.get("tx_hash")
        formatted_logs.append(f"{ts} | {step} | {tx}")

    # JSON‑friendly response for FastAPI / Swagger
    # Shape is aligned with the React UI expectations (decision, risk_scores, logs, tx_hashes, llm_explanation)
    return {
        "mode": mode,
        "decision": decision,
        "final_score": score,
        "reasons": reasons,
        "financial_result": financial,
        "unit_result": unit,
        "risk_scores": result.get("risk_scores"),
        "llm_explanation": result.get("llm_explanation"),
        "logs": formatted_logs,
        "tx_hashes": result.get("tx_hashes", []),
    }


# --------------------------------------------------
if __name__ == "__main__":
    build_graph()
    print("Workflow graph generated successfully!")