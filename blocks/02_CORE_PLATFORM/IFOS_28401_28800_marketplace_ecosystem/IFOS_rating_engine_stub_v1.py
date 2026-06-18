# IFOS Rating Engine Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def aggregate(reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not reviews:
        return {"avg": 0.0, "count": 0, "distribution": {str(i):0 for i in range(1,6)}}
    dist = {i:0 for i in range(1,6)}
    total = 0.0
    weight_sum = 0.0
    for r in reviews:
        stars = int(r.get("stars",0))
        stars = max(1, min(5, stars))
        w = 1.5 if r.get("verified_install") else 1.0
        dist[stars] += 1
        total += stars * w
        weight_sum += w
    avg = total / max(1e-9, weight_sum)
    return {"avg": round(avg,2), "count": len(reviews), "distribution": {str(k):v for k,v in dist.items()}}
