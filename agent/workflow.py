from langgraph.graph import StateGraph
from agent.state import AgentState
from agent.aggregator import aggregate_results
from blockchain.logger import log_step

from tools.financial_trends import FinancialTrendAnalyzer
from tools.unit_economics import UnitEconomicsEngine
from schemas.financial_input import FinancialInput
from schemas.economics_input import UnitEconomicsInput


# --------------------------------------------------
# Financial Analysis Node
# --------------------------------------------------
def financial_node(state: AgentState):

    # Log start
    state = log_step(state, "Financial Analysis Started")

    analyzer = FinancialTrendAnalyzer()
    financial_input = FinancialInput(**state["startup_data"])
    result = analyzer.analyze(financial_input)

    state["financial_result"] = result

    # Log completion
    state = log_step(state, "Financial Analysis Completed")

    return state


# --------------------------------------------------
# Unit Economics Node
# --------------------------------------------------
def unit_node(state: AgentState):

    # Log start
    state = log_step(state, "Unit Economics Analysis Started")

    engine = UnitEconomicsEngine()
    unit_input = UnitEconomicsInput(**state["startup_data"])
    result = engine.analyze(unit_input)

    state["unit_result"] = result

    # Log completion
    state = log_step(state, "Unit Economics Analysis Completed")

    return state


# --------------------------------------------------
# Build Graph
# --------------------------------------------------
def build_graph():

    builder = StateGraph(AgentState)

    # Add Nodes
    builder.add_node("financial", financial_node)
    builder.add_node("unit", unit_node)
    builder.add_node("aggregate", aggregate_results)

    # Entry point
    builder.set_entry_point("financial")

    # Edges
    builder.add_edge("financial", "unit")
    builder.add_edge("unit", "aggregate")

    graph = builder.compile()

    # Generate workflow diagram (Mermaid)
    graph.get_graph().draw_mermaid_png(
        output_file_path="workflow.png"
    )

    return graph


# --------------------------------------------------
# Run directly (optional)

def run_agent(input_data):
    print("Agent running with:", input_data)
    return "Agent executed"
# --------------------------------------------------
if __name__ == "__main__":
    build_graph()
    print("Workflow graph generated successfully!")