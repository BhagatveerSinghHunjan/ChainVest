import streamlit as st
from agent.workflow import run_agent

# ------------------------------------
# Page Configuration
# ------------------------------------

st.set_page_config(
    page_title="ChainVest",
    layout="wide"
)

st.title("🔗 ChainVest")
st.subheader("Blockchain Verified AI Financial Decision Engine")

st.markdown(
"""
ChainVest evaluates startup financial health using a **multi-step AI agent workflow**.

Each step of the analysis is **logged on-chain**, creating a **transparent and verifiable audit trail**.
"""
)

st.divider()

# ------------------------------------
# Mode Selection
# ------------------------------------

mode = st.selectbox(
    "Select Analysis Mode",
    [
        "Startup Risk",
        "Business Loan",
        "VC Investment"
    ]
)

st.divider()

# ------------------------------------
# Financial Inputs
# ------------------------------------

st.subheader("📊 Financial Inputs")

col1, col2, col3 = st.columns(3)

with col1:
    revenue = st.number_input("Monthly Revenue", min_value=0.0)

with col2:
    burn = st.number_input("Monthly Burn", min_value=0.0)

with col3:
    cash = st.number_input("Cash Available", min_value=0.0)

st.divider()

# ------------------------------------
# Run Analysis
# ------------------------------------

if st.button("🚀 Run ChainVest Analysis"):

    if revenue == 0 or burn == 0 or cash == 0:
        st.warning("Please enter all financial inputs before running analysis.")

    else:

        with st.spinner("Running AI agent workflow..."):

            # Create state object expected by run_agent()
            state = {
                "mode": mode,
                "revenue": revenue,
                "burn": burn,
                "cash": cash,
                "tool_results": {},
                "logs": [],
                "tx_hashes": [],
                "decision": None
            }

            # Run agent workflow
            result = run_agent(state)

        st.success("Analysis Complete")

        st.divider()

        # ------------------------------------
        # Final Decision
        # ------------------------------------

        st.subheader("📊 Final Decision")

        st.write("Decision:", result.get("decision", "N/A"))

        # Show runway if financial tool exists
        if "financial" in result.get("tool_results", {}):
            runway = result["tool_results"]["financial"].get("runway", None)
            if runway is not None:
                st.write("Runway (months):", round(runway, 2))

        st.divider()

        # ------------------------------------
        # Agent Logs
        # ------------------------------------

        st.subheader("🧾 Agent Execution Logs")

        if "logs" in result:
            for log in result["logs"]:
                st.write(f"• {log}")

        st.divider()

        # ------------------------------------
        # Blockchain TX Hashes
        # ------------------------------------

        st.subheader("🔗 Blockchain Transaction Hashes")

        if "tx_hashes" in result:
            for tx in result["tx_hashes"]:
                st.code(tx)

        st.divider()

        # ------------------------------------
        # Debug Tool Results (Optional)
        # ------------------------------------

        with st.expander("🔍 Detailed Tool Results"):
            st.json(result.get("tool_results", {}))