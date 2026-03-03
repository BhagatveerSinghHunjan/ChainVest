from typing import TypedDict, Optional, Dict, List


class AgentState(TypedDict):
    # Input
    startup_data: Dict

    # Tool Outputs
    financial_result: Optional[Dict]
    unit_result: Optional[Dict]

    # Aggregation
    final_score: Optional[float]

    # Final Output
    decision: Optional[str]

    # Stage 3 Additions
    logs: List[Dict]
    tx_hashes: List[str]
    next_action: Optional[str]
    terminated: bool