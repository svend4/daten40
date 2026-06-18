# IFOS SLO Evaluator Skeleton v1
from __future__ import annotations
from typing import Dict, Any

def evaluate_slo(slo: Dict[str, Any], sli_value: float) -> Dict[str, Any]:
    op = slo["target"]["operator"]
    target = float(slo["target"]["value"])
    ok = (sli_value >= target) if op == ">=" else (sli_value <= target)
    return {
        "slo_id": slo["slo_id"],
        "window": slo.get("window",""),
        "sli_value": sli_value,
        "target": target,
        "status": "pass" if ok else "breach",
        "action": slo["breach"]["action_on_breach"] if not ok else "none"
    }
