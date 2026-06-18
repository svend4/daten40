# IFOS Compatibility Scorer Stub v1
from __future__ import annotations
from typing import Dict, Any

def score_variant(variant: Dict[str, Any], profile: Dict[str, Any], signals: Dict[str, Any]) -> Dict[str, Any]:
    # Minimal heuristic scoring (stub). Real system uses weights and receipts/trust.
    score = 50.0
    reasons = []
    req = variant.get("requirements", {})
    if req.get("hosting") and profile.get("hosting") and req["hosting"] == profile["hosting"]:
        score += 15; reasons.append("hosting matches")
    q = variant.get("quality_level","L0")
    q_map={"L0":0,"L1":5,"L2":10,"L3":20,"L4":25,"L5":30}
    score += q_map.get(q,0); reasons.append(f"quality {q}")
    if signals.get("dry_run_supported"): score += 5; reasons.append("dry_run supported")
    if signals.get("recent_receipt_ok"): score += 10; reasons.append("recent receipt ok")
    return {"score": max(0.0, min(100.0, score)), "reasons": reasons}
