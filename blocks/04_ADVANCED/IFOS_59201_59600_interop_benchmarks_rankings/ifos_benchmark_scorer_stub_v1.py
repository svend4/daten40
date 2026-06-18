# ifos_benchmark_scorer_stub_v1.py
from __future__ import annotations
from typing import Dict

def score(metrics: Dict, weights: Dict) -> float:
    s=0.0
    wsum=0.0
    for k,w in weights.items():
        v=metrics.get(k)
        if v is None: 
            continue
        s += float(v)*float(w)
        wsum += float(w)
    return s/wsum if wsum else 0.0
