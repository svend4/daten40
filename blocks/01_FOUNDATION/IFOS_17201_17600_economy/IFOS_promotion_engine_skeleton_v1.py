# IFOS Promotion Engine Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List

def apply_promotion_rules(asset_metrics: Dict[str, Any], rules: List[Dict[str, Any]]) -> Dict[str, Any]:
    boost = 1.0
    badges = []
    suppressed = False
    featured_in = []

    for r in sorted(rules or [], key=lambda x: x.get("priority", 100)):
        if not r.get("enabled", False):
            continue
        c = r.get("conditions", {}) or {}
        ok = True
        if "min_evidence_score" in c and asset_metrics.get("evidence_score", 0) < c["min_evidence_score"]:
            ok = False
        if "min_install_success_rate" in c and asset_metrics.get("install_success_rate", 0) < c["min_install_success_rate"]:
            ok = False
        if "max_dispute_rate" in c and asset_metrics.get("dispute_rate", 0) > c["max_dispute_rate"]:
            ok = False
        if "min_docs_score" in c and asset_metrics.get("docs_score", 0) < c["min_docs_score"]:
            ok = False

        if ok:
            a = r.get("actions", {}) or {}
            boost *= float(a.get("boost", 1.0))
            if a.get("badge"):
                badges.append(a["badge"])
            featured_in += (a.get("feature_in", []) or [])
            suppressed = suppressed or bool(a.get("suppress", False))

    return {"boost":boost,"badges":sorted(set(badges)),"featured_in":sorted(set(featured_in)),"suppressed":suppressed}
