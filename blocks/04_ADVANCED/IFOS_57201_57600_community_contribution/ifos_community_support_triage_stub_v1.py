# ifos_community_support_triage_stub_v1.py
from __future__ import annotations
from typing import Dict

def triage(ticket: Dict) -> str:
    text=(ticket.get("text") or "").lower()
    if "timeout" in text or "error" in text:
        return "bug"
    if "how" in text or "как" in text:
        return "question"
    return "feature_request"
