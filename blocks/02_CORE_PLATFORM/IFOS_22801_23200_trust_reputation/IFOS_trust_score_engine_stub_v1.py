# IFOS Trust Score Engine Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def compute_trust_overall(signals: List[Dict[str, Any]]) -> float:
    # Very simple weighted example. Replace with learned/robust model later.
    weights = {
        "stability_fail_ratio": 0.35,
        "security_signed": 0.20,
        "security_sbom": 0.15,
        "adoption_installs": 0.10,
        "incident_count": 0.10,
        "rollback_rate": 0.10,
    }
    score = 0.0
    total = 0.0
    for s in signals:
        w = weights.get(s["type"], 0.0)
        if w <= 0: 
            continue
        val = s["value"]
        if s["type"] == "stability_fail_ratio":
            # lower is better: map 0..0.05 -> 1..0
            val = max(0.0, min(1.0, 1.0 - float(val)/0.05))
        elif isinstance(val, bool):
            val = 1.0 if val else 0.0
        elif s["type"] == "adoption_installs":
            val = max(0.0, min(1.0, float(val)/500.0))
        elif s["type"] in ("incident_count","rollback_rate"):
            val = 1.0 - max(0.0, min(1.0, float(val)/10.0))
        score += w * float(val) * float(s.get("confidence",1.0))
        total += w
    return round(score/total, 4) if total>0 else 0.0
