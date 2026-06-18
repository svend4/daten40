# ifos_entity_linker_stub_v1.py
from __future__ import annotations
from typing import Dict, List, Tuple

def link(candidates: List[Dict]) -> List[Tuple[str,str,float]]:
    # returns pairs (record_id_a, record_id_b, score)
    links=[]
    for i in range(len(candidates)):
        for j in range(i+1,len(candidates)):
            a,b=candidates[i],candidates[j]
            score=0.0
            if a.get("email") and a.get("email")==b.get("email"): score=0.95
            elif a.get("name") and b.get("name") and a["name"].lower()==b["name"].lower(): score=0.6
            if score>0: links.append((a.get("record_id",""), b.get("record_id",""), score))
    return links
