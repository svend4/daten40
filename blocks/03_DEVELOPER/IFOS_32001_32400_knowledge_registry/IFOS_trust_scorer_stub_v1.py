# IFOS Trust Scorer Stub v1
from __future__ import annotations
from typing import Dict, Any, List

WEIGHTS = {
    "maintainer_verified": 0.25,
    "signed_build": 0.15,
    "known_vulns": 0.20,
    "review_quality": 0.15,
    "doc_completeness": 0.10,
    "license_clarity": 0.10,
    "supply_chain_risk": 0.05,
}

def compute_trust_score(signals: List[Dict[str, Any]], baseline: float = 0.5) -> float:
    score = baseline
    for s in signals:
        kind=s.get("kind")
        w=WEIGHTS.get(kind, 0.0) * float(s.get("weight", 1.0))
        val=s.get("value")
        # Heuristic mapping
        if kind == "known_vulns":
            # higher vulns -> penalty
            n = int(val.get("count", 0)) if isinstance(val, dict) else int(val or 0)
            score -= min(0.3, 0.05 * n) * w
        elif kind in ("maintainer_verified","signed_build","license_clarity"):
            score += (1.0 if val in (True, "true", 1) else 0.0) * w
        elif kind == "doc_completeness":
            if isinstance(val, dict):
                score += (1.0 if val.get("quickstart") else 0.0) * w
        elif kind == "supply_chain_risk":
            score -= (1.0 if val in (True, "high") else 0.0) * w
        else:
            # generic: assume numeric 0..1
            try:
                score += float(val) * w
            except Exception:
                pass
    return max(0.0, min(1.0, round(score, 3)))
