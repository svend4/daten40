# IFOS Merge Engine Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def merge_lists(a: List[Any], b: List[Any]) -> List[Any]:
    out=[]
    seen=set()
    for x in a+b:
        k=str(x)
        if k in seen:
            continue
        seen.add(k)
        out.append(x)
    return out

def merge(primary: Dict[str, Any], secondary: Dict[str, Any]) -> Dict[str, Any]:
    merged=dict(primary)
    merged["capabilities"]=merge_lists(primary.get("capabilities", []), secondary.get("capabilities", []))
    merged.setdefault("aliases", [])
    merged["aliases"]=merge_lists(merged["aliases"], [secondary.get("title")])
    return merged
