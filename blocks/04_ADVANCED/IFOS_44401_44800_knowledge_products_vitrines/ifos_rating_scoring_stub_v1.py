# ifos_rating_scoring_stub_v1.py
from __future__ import annotations
from typing import Dict

def score(signals: Dict[str,float], weights: Dict[str,float]) -> float:
    s=0.0
    for k,w in weights.items():
        s += w*float(signals.get(k,0.0))
    return max(0.0, min(1.0, s))
