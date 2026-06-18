# IFOS Vitrine Builder Skeleton v1 (Coverage + constraints, explainable)
from __future__ import annotations
from typing import List, Dict, Any, Tuple

STAGES = ["ingest","transform","store","notify","monitor","admin"]

def covers(bundle: Dict[str, Any]) -> List[str]:
    # bundle advertises coverage stages (MVP)
    return bundle.get("coverage_stages") or []

def score_bundle(bundle: Dict[str, Any], weights: Dict[str,float]) -> float:
    # simple weighted score: trust + avg component rating - penalties
    trust = float(bundle.get("trust_score",0))
    comp = float(bundle.get("avg_component_rating",0))
    risk_penalty = 0.0
    flags = bundle.get("flags") or {}
    if flags.get("money"): risk_penalty += 10.0
    if flags.get("security_sensitive"): risk_penalty += 15.0
    if flags.get("pii"): risk_penalty += 12.0
    return weights.get("trust",0.6)*trust + weights.get("component",0.4)*comp - risk_penalty

def build_vitrine(domain: str, bundles: List[Dict[str, Any]], constraints: Dict[str, Any]) -> Dict[str, Any]:
    min_trust = float(constraints.get("min_trust_score",70))
    min_comp = float(constraints.get("min_component_rating",75))
    deny_flags = constraints.get("deny_flags") or {}
    require_signed = bool(constraints.get("require_signed", False))

    # filter by constraints
    eligible = []
    for b in bundles:
        if b.get("domain") != domain: 
            continue
        if float(b.get("trust_score",0)) < min_trust: 
            continue
        if float(b.get("avg_component_rating",0)) < min_comp:
            continue
        flags = b.get("flags") or {}
        bad = any(deny_flags.get(k, False) and flags.get(k, False) for k in ["pii","money","security_sensitive"])
        if bad: 
            continue
        if require_signed and not b.get("signed", False):
            continue
        eligible.append(b)

    # greedy coverage
    selected = []
    covered = set()
    weights = {"trust":0.6, "component":0.4}
    while len(covered) < len(STAGES):
        best = None
        best_gain = -1
        best_score = -1e9
        for b in eligible:
            if b in selected: 
                continue
            stage_gain = len(set(covers(b)) - covered)
            if stage_gain <= 0:
                continue
            s = score_bundle(b, weights)
            # prefer higher gain first, then score
            if (stage_gain > best_gain) or (stage_gain == best_gain and s > best_score):
                best = b
                best_gain = stage_gain
                best_score = s
        if not best:
            break
        selected.append(best)
        covered |= set(covers(best))

    return {
        "domain": domain,
        "selected_bundles": [b["id"] for b in selected],
        "coverage": sorted(list(covered)),
        "notes": "Greedy coverage under constraints; explainable selection. Add transforms/manual steps if coverage incomplete."
    }

if __name__ == "__main__":
    demo = [
        {"id":"bundle.travelhub.core","domain":"travel","trust_score":82,"avg_component_rating":80,"signed":False,"flags":{"money":False},"coverage_stages":["ingest","store","admin"]},
        {"id":"bundle.travelhub.alerts","domain":"travel","trust_score":78,"avg_component_rating":79,"signed":False,"flags":{"money":False},"coverage_stages":["notify","monitor"]},
        {"id":"bundle.travelhub.transform","domain":"travel","trust_score":75,"avg_component_rating":77,"signed":False,"flags":{"money":False},"coverage_stages":["transform"]},
    ]
    print(build_vitrine("travel", demo, {"min_trust_score":70,"min_component_rating":75,"deny_flags":{"pii":True}}))
