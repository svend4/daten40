# IFOS Trust Score Engine Stub v1
from __future__ import annotations
from typing import Dict, Any

def compute(signals: Dict[str, Any]) -> float:
    # very simple weighted score
    s=0.0
    s += 0.25 * (1.0 if signals.get("signed") else 0.0)
    s += 0.15 * (1.0 if signals.get("sbom") else 0.0)
    s += 0.15 * (1.0 if signals.get("attested") else 0.0)
    vuln=signals.get("vuln")
    if vuln=="block": s += 0.0
    elif vuln=="warn": s += 0.10
    else: s += 0.15
    s += 0.35 * float(signals.get("success_rate", 0.0) or 0.0)
    return max(0.0, min(1.0, s))
