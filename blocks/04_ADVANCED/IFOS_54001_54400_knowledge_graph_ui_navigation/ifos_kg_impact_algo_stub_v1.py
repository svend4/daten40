# ifos_kg_impact_algo_stub_v1.py
from __future__ import annotations
from typing import Dict, List, Set, Tuple

def impact(start: str, edges: List[Dict], depth: int = 4) -> Set[str]:
    # BFS over outgoing edges (directed)
    adj={}
    for e in edges:
        if e.get("directed") and e.get("from"):
            adj.setdefault(e["from"], []).append(e["to"])
    seen=set([start])
    frontier=[start]
    for _ in range(depth):
        nxt=[]
        for u in frontier:
            for v in adj.get(u, []):
                if v not in seen:
                    seen.add(v); nxt.append(v)
        frontier=nxt
        if not frontier: break
    return seen
