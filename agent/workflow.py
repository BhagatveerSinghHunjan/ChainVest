from langgraph.graph import END, StateGraph

from agent.aggregator import aggregate_results
from agent.llm_reasoning import llm_reasoning_node
from agent.state import AgentState
from audit.auditor import audit_step
from blockchain.logger import log_to_chain
from schemas.economics_input import UnitEconomicsInput
from schemas.financial_input import FinancialInput
from tools.financial_trends import FinancialTrendAnalyzer
from tools.unit_economics import UnitEconomicsEngine
from weil_mcp.chainvest_mcp import evaluate_startup


def financial_node(state: AgentState):
    state = log_to_chain(state, "Financial Analysis Started")

    analyzer = FinancialTrendAnalyzer()
    financial_input = FinancialInput(**state["startup_data"])
    result = analyzer.analyze(financial_input)
    state["financial_result"] = result

    latest_revenue = state["startup_data"]["monthly_revenue"][-1]
    latest_burn = state["startup_data"]["monthly_burn"][-1]
    cash = state["startup_data"]["cash_on_hand"]
    state["mcp_result"] = evaluate_startup(latest_revenue, latest_burn, cash)

    state = log_to_chain(state, "Financial Analysis Completed", output_data=result)
    state = audit_step(state, "Financial Analysis Completed")
    return state


def unit_node(state: AgentState):
    state = log_to_chain(state, "Unit Economics Analysis Started")

    engine = UnitEconomicsEngine()
    unit_input = UnitEconomicsInput(**state["startup_data"])
    result = engine.analyze(unit_input)
    state["unit_result"] = result

    state = log_to_chain(state, "Unit Economics Analysis Completed", output_data=result)
    state = audit_step(state, "Unit Economics Analysis Completed")
    return state


def aggregation_node(state: AgentState):
    state = aggregate_results(state)
    state = log_to_chain(state, "Aggregation Completed", output_data=state["risk_scores"])
    state = audit_step(state, "Aggregation Completed")
    return state


def llm_node(state: AgentState):
    state = llm_reasoning_node(state)
    state = log_to_chain(
        state,
        "LLM Reasoning Executed",
        output_data=state.get("llm_explanation"),
    )
    state = audit_step(state, "LLM Reasoning Executed")
    return state


def final_node(state: AgentState):
    state = log_to_chain(
        state,
        "Final Decision Generated",
        output_data={"decision": state["decision"]},
    )
    state = audit_step(state, "Final Decision Generated")
    state["finished"] = True
    return state


def build_graph():
    builder = StateGraph(AgentState)
    builder.add_node("financial", financial_node)
    builder.add_node("unit", unit_node)
    builder.add_node("aggregate", aggregation_node)
    builder.add_node("llm_reasoning", llm_node)
    builder.add_node("finalize", final_node)

    builder.set_entry_point("financial")
    builder.add_edge("financial", "unit")
    builder.add_edge("unit", "aggregate")
    builder.add_edge("aggregate", "llm_reasoning")
    builder.add_edge("llm_reasoning", "finalize")
    builder.add_edge("finalize", END)
    return builder.compile()


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
    avg_revenue = sum(monthly_revenue) / len(monthly_revenue) if monthly_revenue else 0.0
    avg_burn = sum(monthly_burn) / len(monthly_burn) if monthly_burn else 0.0

    derived_ltv = max(avg_revenue * 8, ltv, 100.0)
    derived_cac = max(avg_burn * 0.5, cac, 50.0)

    startup_data = {
        "monthly_revenue": monthly_revenue,
        "monthly_burn": monthly_burn,
        "cash_on_hand": cash_on_hand,
        "ltv": derived_ltv,
        "cac": derived_cac,
        "gross_margin": gross_margin,
        "monthly_new_customers": monthly_new_customers,
    }

    initial_state: AgentState = {
        "mode": mode,
        "startup_data": startup_data,
        "financial_result": None,
        "unit_result": None,
        "mcp_result": None,
        "final_score": None,
        "risk_scores": None,
        "decision": None,
        "llm_explanation": None,
        "logs": [],
        "tx_hashes": [],
        "audit_logs": [],
        "next_action": None,
        "terminated": False,
        "finished": False,
    }

    graph = build_graph()
    result = graph.invoke(initial_state)

    return {
        "mode": result.get("mode", mode),
        "decision": result["decision"],
        "final_score": result["final_score"],
        "financial_result": result["financial_result"],
        "unit_result": result["unit_result"],
        "mcp_result": result.get("mcp_result"),
        "risk_scores": result.get("risk_scores"),
        "llm_explanation": result.get("llm_explanation"),
        "logs": result.get("logs"),
        "tx_hashes": result.get("tx_hashes"),
        "audit_logs": result.get("audit_logs"),
    }


if __name__ == "__main__":
    print("Workflow ready.")
