# ifos_kg_node_ranker_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def rank_nodes(nodes: List[Dict]) -> List[Dict]:
    # placeholder: put nodes with 'risk' meta first
    def score(n):
        m=n.get("meta",{})
        return 1 if m.get("risk") else 0
    return sorted(nodes, key=score, reverse=True)
