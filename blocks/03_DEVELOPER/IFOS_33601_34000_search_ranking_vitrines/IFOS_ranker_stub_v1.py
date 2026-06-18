# IFOS Ranker Stub v1
from __future__ import annotations
from typing import Dict, Any

def score(hit: Dict[str, Any], text_rel: float, weights: Dict[str, float]) -> float:
    sig=hit.get("signals", {})
    def g(k, default=0.0):
        v=sig.get(k)
        return float(v) if v is not None else float(default)
    total=0.0
    total += weights.get("text_relevance",0.0) * text_rel
    total += weights.get("dq_overall",0.0) * g("dq_overall")
    total += weights.get("trust",0.0) * g("trust")
    total += weights.get("installability",0.0) * g("installability")
    total += weights.get("success_rate",0.0) * g("success_rate")
    # freshness: invert days
    fd=sig.get("freshness_days")
    freshness = 1.0/(1.0+float(fd)) if fd is not None else 0.0
    total += weights.get("freshness",0.0) * freshness
    total += weights.get("popularity",0.0) * g("popularity")
    return total
