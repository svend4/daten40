# ifos_ranker_stub_v1.py
from __future__ import annotations
from typing import List, Dict

def rrf_merge(a: List[Dict], b: List[Dict], k: int = 50) -> List[Dict]:
    # Reciprocal Rank Fusion stub
    scores={}
    def add(list_, w=1.0):
        for idx,h in enumerate(list_, start=1):
            item=h["item_id"]
            scores[item]=scores.get(item,0.0)+w*(1.0/(60+idx))
    add(a,1.0); add(b,1.0)
    merged=sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]
    return [{"item_id":i,"score":s} for i,s in merged]
