from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.aggregator import aggregate_results
from blockchain.logger import log_step
from agent.llm_reasoning import llm_reasoning_node

from tools.financial_trends import FinancialTrendAnalyzer
from tools.unit_economics import UnitEconomicsEngine
from schemas.financial_input import FinancialInput
from schemas.economics_input import UnitEconomicsInput


# --------------------------------------------------
# Financial Analysis Node
# --------------------------------------------------
def financial_node(state: AgentState):

    state = log_step(state, "Financial Analysis Started")

    analyzer = FinancialTrendAnalyzer()
    financial_input = FinancialInput(**state["startup_data"])
    result = analyzer.analyze(financial_input)

    state["financial_result"] = result

    state = log_step(state, "Financial Analysis Completed")

    return state


# --------------------------------------------------
# Unit Economics Node
# --------------------------------------------------
def unit_node(state: AgentState):

    state = log_step(state, "Unit Economics Analysis Started")

    engine = UnitEconomicsEngine()
    unit_input = UnitEconomicsInput(**state["startup_data"])
    result = engine.analyze(unit_input)

    state["unit_result"] = result

    state = log_step(state, "Unit Economics Analysis Completed")

    return state


# --------------------------------------------------
# Final Node (NEW - Required)
# --------------------------------------------------
def final_node(state: AgentState):

    state = log_step(state, "Final Decision Generated")

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
# Run directly (optional)
# --------------------------------------------------
def run_agent(input_data):
    print("Agent running with:", input_data)
    return "Agent executed"


# --------------------------------------------------
if __name__ == "__main__":
    build_graph()
    print("Workflow graph generated successfully!")