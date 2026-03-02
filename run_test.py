from agent.workflow import build_graph

# Combine all startup data into ONE dictionary
startup_data = {
    "monthly_revenue": [100,110,120,130,140,150,160,170,180,190,200,210],
    "monthly_burn": [80,85,90,95,100,105,110,115,120,125,130,135],
    "cash_on_hand": 500,
    "ltv": 900,
    "cac": 300,
    "gross_margin": 60,
    "monthly_new_customers": 50
}

graph = build_graph()

initial_state = {
    "startup_data": startup_data,
    "financial_result": None,
    "unit_result": None,
    "final_score": None,
    "decision": None
}

result = graph.invoke(initial_state)

print("\n--- FINAL DECISION ENGINE OUTPUT ---")
print("Final Score:", result["final_score"])
print("Decision:", result["decision"])

if result["decision"] == "REJECT":
    print("Reason: Low runway or unstable financial metrics.")
elif result["decision"] == "REVIEW":
    print("Reason: Moderate financial health, needs further analysis.")
else:
    print("Reason: Strong financial and unit economics performance.")