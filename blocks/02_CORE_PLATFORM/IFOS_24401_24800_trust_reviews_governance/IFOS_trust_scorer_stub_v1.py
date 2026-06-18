# IFOS Trust Scorer Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def compute_trust_score(entity_id: str, receipts: List[Dict[str, Any]], publisher: Dict[str, Any], reviews: List[Dict[str, Any]], incidents: Dict[str, Any]) -> Dict[str, Any]:
    score = 50.0
    reasons=[]
    # receipts
    ok = sum(1 for r in receipts if r.get("result")=="success")
    if ok:
        score += min(30.0, ok*10.0); reasons.append("receipts success")
    # publisher verification
    lvl = (publisher.get("verification_level") if publisher else "unverified")
    bonus={"unverified":0,"domain_verified":10,"org_verified":15,"signed":20}.get(lvl,0)
    score += bonus; reasons.append(f"publisher {lvl}")
    # reviews (ignore spammy)
    clean=[rv for rv in reviews if (rv.get("spam_score",0.0) < 0.5)]
    if clean:
        score += min(15.0, len(clean)*3.0); reasons.append("clean reviews")
    # incidents / abuse
    if incidents.get("incidents_30d",0)>0:
        score -= 20.0; reasons.append("recent incidents")
    return {"score": max(0.0, min(100.0, score)), "reasons": reasons}
