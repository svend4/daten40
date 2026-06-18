# IFOS Review Moderation Stub v1
from __future__ import annotations
from typing import Dict, Any

BANNED = {"scam","malware","virus","hate"}

def moderate_review(review: Dict[str, Any]) -> str:
    text=(review.get("text") or "").lower()
    if any(b in text for b in BANNED):
        return "quarantined"
    if len(text) < 20:
        return "quarantined"
    return "approved"
