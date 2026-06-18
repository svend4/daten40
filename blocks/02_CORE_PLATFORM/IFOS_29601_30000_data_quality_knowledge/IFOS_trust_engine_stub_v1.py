# IFOS Trust Engine Stub v1
from __future__ import annotations
from typing import Dict, Any

def compute_trust(factors: Dict[str, float], weights: Dict[str, float]) -> float:
    score = 0.0
    wsum = 0.0
    for k,v in factors.items():
        w = float(weights.get(k, 0.0))
        score += float(v) * w
        wsum += w
    return score / wsum if wsum else 0.0
