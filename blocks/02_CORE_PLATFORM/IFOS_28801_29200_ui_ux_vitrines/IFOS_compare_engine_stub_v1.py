# IFOS Compare Engine Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def score_item(item: Dict[str, Any], columns: List[Dict[str, Any]]) -> float:
    # weighted sum; assumes numeric fields are present
    total = 0.0
    wsum = 0.0
    for c in columns:
        field = c.get("field")
        w = float(c.get("weight", 0.0) or 0.0)
        val = item.get(field)
        if isinstance(val, (int, float)):
            total += float(val) * w
            wsum += w
    return total / wsum if wsum else 0.0

def run_compare(view: Dict[str, Any], items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    cols = view.get("columns",[]) or []
    scored = []
    for it in items:
        s = score_item(it, cols)
        scored.append({"item": it, "score": s})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored
