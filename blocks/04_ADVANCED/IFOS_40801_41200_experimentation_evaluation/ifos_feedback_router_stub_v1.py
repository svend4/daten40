# ifos_feedback_router_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def route(feedback: Dict[str, Any]) -> str:
    reason=feedback.get("reason","other")
    if reason in ("wrong","incomplete"):
        return "data_or_logic_issue"
    if reason in ("too_expensive","too_slow"):
        return "performance_finops"
    if reason == "hard_to_use":
        return "ux_flow"
    return "triage"
