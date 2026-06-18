# IFOS Ranking Engine Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List
import math

def wilson_interval(p: float, n: int, z: float=1.96):
    if n == 0: return (0.0, 0.0)
    denom = 1 + z*z/n
    center = (p + z*z/(2*n)) / denom
    margin = (z * math.sqrt((p*(1-p) + z*z/(4*n))/n)) / denom
    return (max(0.0, center - margin), min(1.0, center + margin))

def compute_evidence_weighted_score(reviews: List[Dict[str, Any]], evidence_map: Dict[str, float]) -> float:
    # evidence_map: review_id -> weight (0..1)
    total_w = 0.0
    total = 0.0
    for rv in reviews or []:
        w = float(evidence_map.get(rv["review_id"], 0.1 if not rv.get("verified_usage") else 1.0))
        total_w += w
        total += w * float(rv.get("stars", 0))
    return (total/total_w) if total_w > 0 else 0.0

def recompute_rating(subject: Dict[str, Any], reviews: List[Dict[str, Any]], evidence_score: float, install_success_rate: float, docs_score: float, dispute_rate: float, fraud_penalty: float) -> Dict[str, Any]:
    stars_avg = (sum(r.get("stars",0) for r in reviews)/len(reviews)) if reviews else 0.0
    dist = {str(i):0 for i in range(1,6)}
    for r in reviews or []:
        dist[str(r.get("stars",0))] = dist.get(str(r.get("stars",0)),0) + 1

    evidence_map = {r["review_id"]:(1.0 if r.get("verified_usage") else 0.1) for r in reviews or []}
    ew = compute_evidence_weighted_score(reviews, evidence_map)

    stars_norm = stars_avg/5.0
    score_norm = 0.35*stars_norm + 0.35*evidence_score + 0.15*install_success_rate + 0.10*docs_score - 0.05*dispute_rate - 0.10*fraud_penalty
    evidence_weighted_score = max(0.0, min(5.0, score_norm*5.0))

    # confidence interval over positive rate (>=4 stars)
    n = len(reviews)
    pos = sum(1 for r in reviews or [] if r.get("stars",0) >= 4)
    low, high = wilson_interval(pos/n if n else 0.0, n)
    return {
        "rating_id":"rat.generated",
        "subject":subject,
        "stars_avg":round(stars_avg,2),
        "count":n,
        "distribution":{int(k):v for k,v in dist.items()},
        "evidence_weighted_score":round(evidence_weighted_score,2),
        "confidence":{"low":round(low*5,2),"high":round(high*5,2),"method":"wilson+evidence"},
        "updated_at":"",
        "version":"1.0.0"
    }
