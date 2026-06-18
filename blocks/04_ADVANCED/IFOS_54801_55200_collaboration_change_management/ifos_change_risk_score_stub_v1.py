# ifos_change_risk_score_stub_v1.py
from __future__ import annotations
from typing import Dict

def score(change: Dict) -> str:
    # Placeholder heuristic
    flags=set(change.get("flags", []))
    if "PII" in flags or "payments" in flags:
        return "high"
    if "auth" in flags or "schema" in flags:
        return "medium"
    return "low"
