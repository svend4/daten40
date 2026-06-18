# IFOS Ranking Engine Stub v1
from __future__ import annotations
from typing import Dict, Any, List, Tuple
import difflib

def text_sim(a: str, b: str) -> float:
    return difflib.SequenceMatcher(a=a.lower(), b=b.lower()).ratio()

def rank_items(query: str, items: List[Dict[str, Any]], context: Dict[str, Any]) -> List[Dict[str, Any]]:
    results=[]
    for it in items:
        score=0.0
        explain=[]
        score += 0.45 * text_sim(query, (it.get("name","")+" "+it.get("summary","")))
        # taxonomy boost
        for p in it.get("taxonomy_paths", []):
            if any(tok in p.lower() for tok in query.lower().split()):
                score += 0.05
                explain.append(f"taxonomy match: {p}")
                break
        # trust
        ts = it.get("trust_score")
        if ts is not None:
            score += 0.25 * float(ts)
            explain.append(f"trust_score={ts}")
        # compatibility fit (very naive)
        if context.get("platform") and any(context["platform"] in p.lower() for p in it.get("taxonomy_paths",[])):
            score += 0.05
            explain.append("context platform boost")
        results.append({"item_id": it["id"], "score": round(min(1.0, score), 3), "explain": explain})
    results.sort(key=lambda x: x["score"], reverse=True)
    return results
