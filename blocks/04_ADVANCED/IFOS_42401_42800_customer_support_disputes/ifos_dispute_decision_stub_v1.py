# ifos_dispute_decision_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def decide(case: Dict[str, Any], evidence_strength: float) -> Dict[str, Any]:
    # simplistic: higher evidence strength -> win
    if evidence_strength >= 0.7:
        return {"outcome":"decline_customer_claim","reason":"evidence_strong"}
    if evidence_strength <= 0.3:
        return {"outcome":"approve_customer_claim","reason":"evidence_weak"}
    return {"outcome":"partial_or_manual","reason":"needs_review"}
