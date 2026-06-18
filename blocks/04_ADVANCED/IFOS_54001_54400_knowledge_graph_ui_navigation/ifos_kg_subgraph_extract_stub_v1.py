# ifos_kg_subgraph_extract_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def extract(nodes: List[Dict], edges: List[Dict], node_ids: set) -> Dict:
    n=[x for x in nodes if x.get("node_id") in node_ids]
    e=[x for x in edges if x.get("from") in node_ids and x.get("to") in node_ids]
    return {"nodes": n, "edges": e}
