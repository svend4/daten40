# ifos_ranker_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def rank(items: List[Dict], weights: Dict[str,float]) -> List[Dict]:
    for it in items:
        s=0.0
        for k,w in weights.items():
            s += w*float(it.get(k,0.0))
        it["score"]=s
    return sorted(items, key=lambda x: x.get("score",0.0), reverse=True)
