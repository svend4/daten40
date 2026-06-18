# IFOS Quality Scorer Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List

DEFAULT_WEIGHTS = {
    "Stability": 0.30,
    "Installability": 0.20,
    "Performance": 0.15,
    "Docs": 0.15,
    "Trust": 0.15,
    "Support": 0.05,
}

def compute_score(components: List[Dict[str, Any]]) -> float:
    total = 0.0
    for c in components:
        total += float(c["value"]) * float(c["weight"])
    return max(0.0, min(1.0, total))

def score_subject(subject: Dict[str, Any], signals: Dict[str, Any]) -> Dict[str, Any]:
    # signals: collected metrics/slo/tests/docs/trust
    components = signals.get("components", [])
    return {
        "score_id": "qscore.generated",
        "subject": subject,
        "score": compute_score(components),
        "components": components,
        "explanation": ["Auto scoring (stub)"],
        "inputs": signals.get("inputs", []),
        "version": "1.0.0",
        "updated_at": ""
    }
