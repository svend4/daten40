# IFOS Reputation Engine Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def compute_reputation(rating: float, evidence_score: float, quality_score: float, counts: Dict[str, int]) -> Dict[str, Any]:
    # Stub: reputation is not a single scalar; keep signals separated
    return {
        "rating": rating,
        "evidence_score": evidence_score,
        "quality_score": quality_score,
        "review_counts": counts,
    }
