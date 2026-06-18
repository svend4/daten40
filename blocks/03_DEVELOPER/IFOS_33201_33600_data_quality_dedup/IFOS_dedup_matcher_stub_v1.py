# IFOS Dedup Matcher Stub v1
from __future__ import annotations
from typing import Dict, Any

def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / max(1, len(a | b))

def similarity(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    cap_a=set(a.get("capabilities", []))
    cap_b=set(b.get("capabilities", []))
    cap_score=jaccard(cap_a, cap_b)
    # naive name score: exact lowercased match
    name_score=1.0 if (a.get("title","").lower()==b.get("title","").lower()) else 0.7
    score=0.6*cap_score + 0.4*name_score
    rec="keep_separate"
    if score>=0.95:
        rec="auto_merge"
    elif score>=0.75:
        rec="review"
    return {"score": round(score,3), "recommendation": rec, "evidence":{"cap_score":cap_score,"name_score":name_score}}
