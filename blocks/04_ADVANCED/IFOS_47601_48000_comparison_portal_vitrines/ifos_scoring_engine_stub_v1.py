# ifos_scoring_engine_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def score(offers: List[Dict], weights: Dict) -> List[Dict]:
    # stub: score by simple inverse price if present
    out=[]
    for o in offers:
        price=o.get("price",{}).get("amount")
        s=1.0/(1.0+float(price)) if price is not None else 0.5
        out.append({**o, "score": s})
    return sorted(out, key=lambda x: x.get("score",0), reverse=True)
