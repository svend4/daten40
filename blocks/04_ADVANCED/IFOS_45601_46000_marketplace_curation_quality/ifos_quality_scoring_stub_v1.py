# ifos_quality_scoring_stub_v1.py
from __future__ import annotations
from typing import Dict

def compute_quality(scores: Dict[str,float], weights: Dict[str,float]) -> float:
    q=0.0
    for k,w in weights.items():
        q += w*float(scores.get(k,0.0))
    return max(0.0, min(1.0, q))
