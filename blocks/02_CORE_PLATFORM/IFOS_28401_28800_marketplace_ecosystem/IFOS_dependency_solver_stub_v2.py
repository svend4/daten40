# IFOS Dependency Solver Stub v2
from __future__ import annotations
from typing import Dict, Any, List, Tuple, Set

def topo_sort(nodes: List[str], edges: List[Tuple[str,str]]) -> List[str]:
    indeg = {n:0 for n in nodes}
    out = {n:[] for n in nodes}
    for a,b in edges:
        out[a].append(b)
        indeg[b] += 1
    q = [n for n in nodes if indeg[n]==0]
    order = []
    while q:
        n = q.pop()
        order.append(n)
        for m in out[n]:
            indeg[m] -= 1
            if indeg[m]==0:
                q.append(m)
    if len(order)!=len(nodes):
        raise ValueError("cycle detected")
    return order

def resolve(graph: Dict[str, Any]) -> Dict[str, Any]:
    # graph: {nodes:[{id,kind,optional}], edges:[{from,to,type}], strategy}
    nodes = [n["id"] for n in graph.get("nodes",[])]
    requires = [(e["from"], e["to"]) for e in graph.get("edges",[]) if e.get("type")=="requires"]
    conflicts = [(e["from"], e["to"]) for e in graph.get("edges",[]) if e.get("type")=="conflicts"]
    # naive conflict check
    conflict_set = set(tuple(c) for c in conflicts)
    if conflict_set:
        return {"ok": False, "reason":"conflicts_present", "conflicts": list(conflict_set)}
    order = topo_sort(nodes, requires)
    return {"ok": True, "install_order": order}
