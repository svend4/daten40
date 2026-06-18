# IFOS Review Anti-Fraud Skeleton v1
# Produces signal scores and recommended actions for a listing.
from __future__ import annotations
from typing import Dict, Any, List
import math
import hashlib

def clamp(x: float, lo: float=0.0, hi: float=100.0) -> float:
    return max(lo, min(hi, x))

def score_no_usage(reviews_count: int, runs_after_install_ratio: float) -> float:
    # If many reviews but almost no runs, suspicious.
    base = math.log(1 + reviews_count) * 15.0
    penalty = (1.0 - runs_after_install_ratio) * 60.0
    return clamp(base + penalty)

def score_text_duplication(dup_ratio: float, reviews_count: int) -> float:
    # high duplication -> suspicious
    base = dup_ratio * 100.0
    boost = math.log(1 + reviews_count) * 5.0
    return clamp(base + boost)

def score_low_context(context_ratio: float, reviews_count: int) -> float:
    # reviews without run_id/version are low value; if too many -> suspicious
    base = (1.0 - context_ratio) * 80.0
    boost = math.log(1 + reviews_count) * 6.0
    return clamp(base + boost)

def recommend_action(max_score: float) -> str:
    if max_score >= 85: return "freeze_score"
    if max_score >= 70: return "moderate"
    if max_score >= 55: return "downweight"
    return "ignore"

def make_signal_id(listing_id: str, kind: str) -> str:
    h = hashlib.sha256((listing_id + ":" + kind).encode("utf-8")).hexdigest()[:10]
    return f"sig.{kind}.{h}"

def compute_signals(listing_id: str, features: Dict[str, Any]) -> List[Dict[str, Any]]:
    reviews = int(features.get("reviews_count", 0))
    dup_ratio = float(features.get("dup_text_ratio", 0.0))
    runs_ratio = float(features.get("runs_after_install_ratio", 1.0))
    ctx_ratio = float(features.get("context_attached_ratio", 1.0))
    window = float(features.get("time_window_hours", 24.0))

    sigs = []

    s1 = score_no_usage(reviews, runs_ratio)
    sigs.append({"signal_kind":"no_usage","score":s1,"features":features,"time_window_hours":window})

    s2 = score_text_duplication(dup_ratio, reviews)
    sigs.append({"signal_kind":"text_duplication","score":s2,"features":features,"time_window_hours":window})

    s3 = score_low_context(ctx_ratio, reviews)
    sigs.append({"signal_kind":"low_context","score":s3,"features":features,"time_window_hours":window})

    max_score = max(s["score"] for s in sigs) if sigs else 0.0
    action = recommend_action(max_score)
    for s in sigs:
        s["signal_id"] = make_signal_id(listing_id, s["signal_kind"])
        s["listing_id"] = listing_id
        s["recommended_action"] = action
        s["method_version"] = "antifraud.v1"
    return sigs

if __name__ == "__main__":
    demo_features = {"reviews_count":120,"dup_text_ratio":0.42,"runs_after_install_ratio":0.05,"context_attached_ratio":0.08,"time_window_hours":24}
    out = compute_signals("lst.super_ai_bundle.001", demo_features)
    for s in out:
        print(s["signal_kind"], s["score"], s["recommended_action"])
