from typing import TypedDict, Optional, Dict


class AgentState(TypedDict):
    startup_data: Dict
    financial_result: Optional[Dict]
    unit_result: Optional[Dict]
    final_score: Optional[float]
    decision: Optional[str]