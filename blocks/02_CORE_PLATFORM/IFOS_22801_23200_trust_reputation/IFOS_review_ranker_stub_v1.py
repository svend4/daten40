# IFOS Review Ranker Stub v1
from __future__ import annotations
from typing import Dict, Any

def rank(review: Dict[str, Any]) -> float:
    # Higher rank for evidence, author reputation, and longer structured text.
    rep = float(review.get("author", {}).get("reputation", 0.0))
    ev = len(review.get("evidence", []))
    txt = len(review.get("text", ""))
    return round(0.4*rep + 0.4*min(1.0, ev/3.0) + 0.2*min(1.0, txt/300.0), 4)
