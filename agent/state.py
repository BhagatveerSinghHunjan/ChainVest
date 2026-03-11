from typing import Dict, List, Optional, TypedDict


class AgentState(TypedDict):
    # Input
    mode: str
    startup_data: Dict

    # Tool Outputs
    financial_result: Optional[Dict]
    unit_result: Optional[Dict]
    mcp_result: Optional[Dict]

    # Aggregation
    final_score: Optional[float]
    risk_scores: Optional[Dict]

    # Final Output
    decision: Optional[str]
    llm_explanation: Optional[Dict]

    # Audit + execution traces
    logs: List[Dict]
    tx_hashes: List[str]
    audit_logs: List[Dict]

    # Workflow control flags
    next_action: Optional[str]
    terminated: bool
    finished: bool
