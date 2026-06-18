# IFOS Anti-Fraud Detector Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def detect_signals(subject_id: str, reviews: List[Dict[str, Any]], verified_ratio: float) -> List[Dict[str, Any]]:
    signals=[]
    if verified_ratio < 0.2 and len(reviews) > 5:
        signals.append({"type":"low_verified_ratio","severity":"high","evidence":[f"ratio={verified_ratio}"]})
    # TODO: velocity spikes, text duplication, ip clustering
    return signals
