# ifos_entity_matcher_stub_v1.py
from __future__ import annotations
from typing import Dict, List, Tuple

def candidates(records: List[Dict]) -> List[Dict]:
    # Placeholder: match by domain if exists
    out=[]
    seen={}
    for r in records:
        dom = (r.get("identifiers") or {}).get("domain")
        if not dom: 
            continue
        if dom in seen:
            out.append({"a": seen[dom], "b": r.get("entity_id"), "score": 0.9, "evidence":["domain_match"]})
        else:
            seen[dom]=r.get("entity_id")
    return out
