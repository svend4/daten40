# IFOS Comparison Engine Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List

def compare(intent: str, candidates: List[Dict[str, Any]], weights: Dict[str, float]) -> Dict[str, Any]:
    # candidates contain scores per criterion in [0..1]
    table=[]
    best_id=None
    best_score=-1.0
    for c in candidates:
        s=0.0
        for k,w in weights.items():
            s += w * float(c.get("scores", {}).get(k, 0.0))
        table.append({"subject_id": c["subject_id"], "score": s, "notes": c.get("notes","")})
        if s > best_score:
            best_score=s
            best_id=c["subject_id"]
    return {"intent": intent, "winner": best_id, "table": sorted(table, key=lambda x: x["score"], reverse=True)}
