# IFOS Economy Anti‑Fraud Engine Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List
import math
import hashlib

def text_fingerprint(t: str) -> str:
    t = (t or "").strip().lower().encode("utf-8")
    return hashlib.sha256(t).hexdigest()[:12]

def analyze_reviews(reviews: List[Dict[str, Any]], window_minutes: int=10) -> List[Dict[str, Any]]:
    # MVP heuristics (timestamps not parsed here; assume list is "recent")
    signals = []
    if len(reviews or []) >= 30:
        verified = sum(1 for r in reviews if r.get("verified_usage"))
        verified_ratio = verified / max(1, len(reviews))
        fps = [text_fingerprint(r.get("text","")) for r in reviews]
        # similarity proxy: many identical fingerprints
        top = max((fps.count(x) for x in set(fps)), default=1)
        similarity = top / max(1, len(fps))
        if verified_ratio < 0.1 and similarity > 0.2:
            signals.append({
                "signal_id":"af.generated",
                "kind":"review_spam",
                "subject":{"kind":"asset","id":"unknown"},
                "severity":"high",
                "features":[
                    {"name":"review_density_10min","value":str(len(reviews)),"weight":0.35,"note":"too many in short time"},
                    {"name":"verified_ratio","value":f"{verified_ratio:.2f}","weight":0.25,"note":"low verified usage"},
                    {"name":"text_similarity","value":f"{similarity:.2f}","weight":0.25,"note":"templated reviews"}
                ],
                "recommended_action":"Hide reviews, freeze rating, require verified usage; send to governance.",
                "generated_at":"",
                "method_version":"antifraud.v1"
            })
    return signals
