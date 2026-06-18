# IFOS Recommendation Ranker Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List

def rank(intent: str, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # candidates already have match/trust/cost signals
    def score(c: Dict[str, Any]) -> float:
        return 0.45*c.get("match",0)+0.35*c.get("trust",0)+0.20*c.get("simplicity",0)-0.15*c.get("risk",0)
    out=[]
    for c in candidates:
        out.append({"subject_id": c["subject_id"], "score": max(0.0, min(1.0, score(c))), "why": c.get("why",[])})
    return sorted(out, key=lambda x: x["score"], reverse=True)
