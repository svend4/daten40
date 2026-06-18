# IFOS Tag Normalizer Skeleton v1
from __future__ import annotations
from typing import Dict, List

def normalize_tags(tags: List[str], alias_map: Dict[str, str], stop_tags: List[str]) -> List[str]:
    out = []
    for t in tags:
        if t is None:
            continue
        t2 = t.strip().lower()
        t2 = "".join(ch if ch.isalnum() else " " for ch in t2)
        t2 = " ".join(t2.split())
        t2 = alias_map.get(t2, t2)
        if t2 and t2 not in stop_tags:
            out.append(t2)
    # unique, stable order
    seen=set()
    res=[]
    for t in out:
        if t not in seen:
            seen.add(t); res.append(t)
    return res
