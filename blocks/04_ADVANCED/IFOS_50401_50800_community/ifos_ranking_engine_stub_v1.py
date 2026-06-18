# ifos_ranking_engine_stub_v1.py
from __future__ import annotations
from typing import Dict

def score(components: Dict[str,float]) -> float:
    # simple weighted sum stub
    w={"quality":0.25,"trust":0.25,"freshness":0.15,"cost":0.10,"fit":0.25}
    return sum(components.get(k,0)*w[k] for k in w)*100
