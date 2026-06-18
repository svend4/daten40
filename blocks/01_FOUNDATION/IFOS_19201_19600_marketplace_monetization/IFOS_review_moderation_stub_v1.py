# IFOS Review Moderation Stub v1
from __future__ import annotations
from typing import Dict, Any

def moderate(review: Dict[str, Any]) -> Dict[str, Any]:
    text = (review.get("text","") or "").lower()
    if "http://" in text or "https://" in text:
        # simplistic spam heuristic
        review["flags"] = ["contains_link"]
    review["status"] = "approved"
    return review
