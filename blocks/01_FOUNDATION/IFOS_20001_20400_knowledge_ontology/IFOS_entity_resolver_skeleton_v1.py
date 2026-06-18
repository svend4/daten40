# IFOS Entity Resolver Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List, Tuple

def similarity(a: Dict[str, Any], b: Dict[str, Any]) -> float:
    # very rough heuristic
    fa = a.get("fingerprints", {})
    fb = b.get("fingerprints", {})
    if fa.get("content_digest") and fa.get("content_digest") == fb.get("content_digest"):
        return 1.0
    score = 0.0
    if fa.get("structure_digest") and fa.get("structure_digest") == fb.get("structure_digest"):
        score += 0.6
    ca=set(a.get("capabilities", [])); cb=set(b.get("capabilities", []))
    if ca and cb:
        score += 0.4 * (len(ca & cb) / max(1, len(ca | cb)))
    return min(1.0, score)

def dedupe(entities: List[Dict[str, Any]], threshold: float = 0.9) -> List[Tuple[str, str, float]]:
    # returns pairs (primary, dup, confidence)
    pairs=[]
    for i in range(len(entities)):
        for j in range(i+1, len(entities)):
            s = similarity(entities[i], entities[j])
            if s >= threshold:
                pairs.append((entities[i]["entity_id"], entities[j]["entity_id"], s))
    return pairs
