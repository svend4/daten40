# IFOS Explainable Ranker Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List

def rank(query: Dict[str, Any], candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Returns list of {entity_id, score, explanation}
    results=[]
    q_tags=set(query.get("tags", []))
    q_caps=set(query.get("capabilities", []))
    for c in candidates:
        tags=set(c.get("tags", []))
        caps=set(c.get("capabilities", []))
        tag_match=len(q_tags & tags) / max(1, len(q_tags))
        cap_match=len(q_caps & caps) / max(1, len(q_caps))
        score=0.4*tag_match+0.6*cap_match
        expl={
            "matches":{"tags":list(q_tags & tags),"capabilities":list(q_caps & caps)},
            "breakdown":[
                {"component":"tag_match","score":0.4*tag_match,"notes":""},
                {"component":"capability_match","score":0.6*cap_match,"notes":""}
            ],
            "penalties":[]
        }
        results.append({"entity_id": c["entity_id"], "score": score, "explanation": expl})
    return sorted(results, key=lambda x: x["score"], reverse=True)
