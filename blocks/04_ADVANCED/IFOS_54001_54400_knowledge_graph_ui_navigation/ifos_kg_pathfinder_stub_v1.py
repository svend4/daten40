# ifos_kg_pathfinder_stub_v1.py
from __future__ import annotations
from collections import deque
from typing import Dict, List, Optional

def shortest_path(start: str, goal: str, edges: List[Dict]) -> Optional[List[str]]:
    adj={}
    for e in edges:
        if e.get("directed"):
            adj.setdefault(e["from"], []).append(e["to"])
    q=deque([start])
    prev={start: None}
    while q:
        u=q.popleft()
        if u==goal: break
        for v in adj.get(u, []):
            if v not in prev:
                prev[v]=u
                q.append(v)
    if goal not in prev: return None
    path=[]
    cur=goal
    while cur is not None:
        path.append(cur)
        cur=prev[cur]
    return list(reversed(path))
