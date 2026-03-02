from langgraph.graph import StateGraph
from agent.state import AgentState
from agent.aggregator import aggregate_results

from tools.financial_trends import FinancialTrendAnalyzer
from tools.unit_economics import UnitEconomicsEngine
from schemas.financial_input import FinancialInput
from schemas.economics_input import UnitEconomicsInput


def financial_node(state: AgentState):
    analyzer = FinancialTrendAnalyzer()
    financial_input = FinancialInput(**state["startup_data"])
    result = analyzer.analyze(financial_input)
    state["financial_result"] = result
    return state


def unit_node(state: AgentState):
    engine = UnitEconomicsEngine()
    unit_input = UnitEconomicsInput(**state["startup_data"])
    result = engine.analyze(unit_input)
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

    graph = builder.compile()

    # Create visual graph using Mermaid (no build tools needed)
    graph.get_graph().draw_mermaid_png(output_file_path="workflow.png")
   

    return graph
if __name__ == "__main__":
    build_graph()
    print("Workflow graph generated successfully!")