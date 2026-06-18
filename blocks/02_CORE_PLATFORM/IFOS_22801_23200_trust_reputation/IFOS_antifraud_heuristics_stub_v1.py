# IFOS AntiFraud Heuristics Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def check(subject_id: str, reviews: List[Dict[str, Any]], installs: int, fail_ratio: float) -> Dict[str, Any]:
    # Simple contradictions and burst checks.
    burst = len(reviews) > max(5, installs * 0.2)  # suspicious if too many reviews compared to installs
    high_5stars = sum(1 for r in reviews if r.get("scores",{}).get("reliability",0) >= 4.8) / max(1,len(reviews))
    contradiction = (high_5stars > 0.7 and fail_ratio > 0.05)
    score = 0.0
    score += 0.5 if burst else 0.0
    score += 0.5 if contradiction else 0.0
    label = "clean"
    if score >= 0.8:
        label = "fraud_likely"
    elif score >= 0.4:
        label = "suspicious"
    return {"subject_id":subject_id,"score":score,"label":label,"signals":[f"burst:{burst}",f"contradiction:{contradiction}"]}
