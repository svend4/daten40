# ifos_anti_gaming_checks_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def anomalies(score_history: List[float]) -> List[str]:
    if not score_history:
        return []
    if len(score_history)>=2 and score_history[-1]-score_history[-2] > 0.25:
        return ["suspicious_spike"]
    return []
