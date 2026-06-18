# IFOS Trust Score Skeleton v1
# Computes a trust score from evidence + reviews + freshness, with explainable breakdown.
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any
import datetime

LEVEL_WEIGHT = {
    "L0_schema": 10,
    "L1_dry_run": 35,
    "L2_integration": 70,
    "L3_production": 100,
}

def clamp(x: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, x))

def evidence_score(evidence_records: List[Dict[str, Any]]) -> float:
    if not evidence_records:
        return 0.0
    # take best 3 records by level, average
    scored = []
    for e in evidence_records:
        level = e.get("level","L0_schema")
        base = LEVEL_WEIGHT.get(level, 0)
        result = e.get("result","FAIL")
        mult = 1.0 if result == "PASS" else (0.6 if result == "WARN" else 0.0)
        # penalize if secret_scan FAIL/WARN
        checks = e.get("checks") or []
        secret = next((c for c in checks if c.get("kind") == "secret_scan"), None)
        if secret and secret.get("status") == "FAIL":
            mult *= 0.3
        scored.append(base * mult)
    scored.sort(reverse=True)
    top = scored[:3]
    return sum(top) / len(top)

def security_score(evidence_records: List[Dict[str, Any]], policy_flags: Dict[str, bool]) -> float:
    # start from 100 and subtract penalties
    score = 100.0
    # policy: if pii then require L2+ to keep score high
    if policy_flags.get("pii"):
        score -= 15.0
    if policy_flags.get("money"):
        score -= 20.0
    if policy_flags.get("security_sensitive"):
        score -= 25.0

    # evidence: if any security_scan FAIL -> big penalty
    for e in evidence_records:
        for c in (e.get("checks") or []):
            if c.get("kind") == "security_scan" and c.get("status") == "FAIL":
                score -= 40.0
            if c.get("kind") == "secret_scan" and c.get("status") == "FAIL":
                score -= 30.0
    return clamp(score)

def popularity_score(reviews: List[Dict[str, Any]]) -> float:
    # simple: rating average + count bonus
    if not reviews:
        return 0.0
    avg = sum(r.get("rating",0) for r in reviews) / len(reviews)
    base = (avg / 5.0) * 80.0
    bonus = min(20.0, len(reviews) * 2.0)  # up to +20
    return clamp(base + bonus)

def freshness_score(updated_at_iso: str, now: datetime.datetime | None = None) -> float:
    now = now or datetime.datetime.utcnow()
    try:
        updated = datetime.datetime.fromisoformat(updated_at_iso.replace("Z",""))
    except Exception:
        return 50.0
    days = (now - updated).days
    # 0 days -> 100, 180 days -> ~50, 365 days -> ~30
    if days <= 0: return 100.0
    if days >= 365: return 30.0
    return clamp(100.0 - (days * 0.19))  # linear MVP

def support_score(publisher_metrics: Dict[str, Any]) -> float:
    # placeholder: use response time / SLA later
    # MVP: if has support_url and avg_response_hours
    if not publisher_metrics:
        return 50.0
    hrs = publisher_metrics.get("avg_response_hours", 999)
    if hrs <= 4: return 95.0
    if hrs <= 24: return 80.0
    if hrs <= 72: return 60.0
    return 40.0

def compute_trust(listing: Dict[str, Any],
                  evidence_records: List[Dict[str, Any]],
                  reviews: List[Dict[str, Any]],
                  publisher_metrics: Dict[str, Any] | None = None) -> Dict[str, Any]:
    ev = evidence_score(evidence_records)
    sec = security_score(evidence_records, listing.get("policy_flags") or {})
    pop = popularity_score(reviews)
    fre = freshness_score(listing.get("updated_at",""), None)
    sup = support_score(publisher_metrics or {})

    # weighted sum
    score = 0.45*ev + 0.25*sec + 0.15*fre + 0.10*sup + 0.05*pop
    explain = [
        f"Evidence={ev:.1f} (weight 45%)",
        f"Security={sec:.1f} (weight 25%)",
        f"Freshness={fre:.1f} (weight 15%)",
        f"Support={sup:.1f} (weight 10%)",
        f"Popularity={pop:.1f} (weight 5%)",
    ]
    return {
        "version":"1.0.0",
        "listing_id": listing.get("listing_id",""),
        "score": round(clamp(score), 2),
        "breakdown": {"evidence": round(ev,2), "security": round(sec,2), "popularity": round(pop,2),
                      "freshness": round(fre,2), "support": round(sup,2)},
        "explain": explain,
        "computed_at": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z",
    }

if __name__ == "__main__":
    # demo run with minimal objects
    import json
    sample_listing = {"listing_id":"lst.demo.1","policy_flags":{"pii":False,"money":False,"security_sensitive":False},
                      "updated_at":"2026-01-01T10:00:00Z"}
    sample_evidence = [{"level":"L1_dry_run","result":"PASS","checks":[{"kind":"secret_scan","status":"PASS"}]}]
    sample_reviews = [{"rating":5},{"rating":4},{"rating":5}]
    print(json.dumps(compute_trust(sample_listing, sample_evidence, sample_reviews), ensure_ascii=False, indent=2))
