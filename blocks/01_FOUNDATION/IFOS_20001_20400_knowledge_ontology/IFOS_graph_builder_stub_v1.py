# IFOS Graph Builder Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def build_graph(entities: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Stub: build edges based on capabilities and known connectors
    nodes=[e["entity_id"] for e in entities]
    edges=[]
    for e in entities:
        for cap in e.get("capabilities", []):
            edges.append({"from": e["entity_id"], "type": "HAS_CAPABILITY", "to": f"capability.{cap}", "weight": 1.0})
    return {"nodes": nodes, "edges": edges}
