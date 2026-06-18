# IFOS Vitrine Builder Stub v1
from __future__ import annotations
from typing import Dict, Any, List
from .IFOS_ranker_stub_v1 import score as score_hit  # type: ignore

def build_auto_vitrine(name: str, docs: List[Dict[str, Any]], ranking_profile: Dict[str, Any], filters: Dict[str, Any]) -> Dict[str, Any]:
    weights=ranking_profile.get("weights", {})
    candidates=[]
    for d in docs:
        if any((k not in d.get("facets", {})) for k in filters.keys()):
            pass
        ok=True
        for k,v in filters.items():
            dv=d.get("facets", {}).get(k)
            if isinstance(v, list):
                if isinstance(dv, list):
                    if not set(v).intersection(set(dv)): ok=False
                else:
                    if dv not in v: ok=False
            else:
                if dv != v: ok=False
        if not ok:
            continue
        text_rel=1.0  # vitrines often are filter-based; text relevance not used
        candidates.append((d, score_hit(d, text_rel, weights)))
    candidates.sort(key=lambda x: x[1], reverse=True)
    items=[]
    for i,(d,s) in enumerate(candidates[:20], start=1):
        items.append({
            "canonical_id": d["canonical_id"],
            "position": i,
            "reason": f"rank_score={round(s,3)}",
            "requirements": {"platform": d.get("facets", {}).get("platform")},
            "one_click_ready": bool(d.get("signals", {}).get("installability",0) >= 0.8),
            "version":"1.0.0"
        })
    return {
        "vitrine_id":"vit:auto:"+name,
        "title":name,
        "kind":"auto",
        "criteria":filters,
        "items":items,
        "updated_at":"",
        "version":"1.0.0"
    }
