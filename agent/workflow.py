from langgraph.graph import StateGraph
from agent.state import AgentState
from agent.planner import decide_next_step
from agent.aggregator import aggregate_results

from tools.financial_trends import analyze_financials
from tools.unit_economics import analyze_unit_economics


def financial_node(state: AgentState):
    result = analyze_financials(state["startup_data"])
    state["financial_result"] = result
    return state


def unit_node(state: AgentState):
    result = analyze_unit_economics(state["startup_data"])
    state["unit_result"] = result
    return state


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("financial", financial_node)
    builder.add_node("unit", unit_node)
    builder.add_node("aggregate", aggregate_results)

    builder.set_entry_point("financial")

    builder.add_edge("financial", "unit")
    builder.add_edge("unit", "aggregate")

    return builder.compile()