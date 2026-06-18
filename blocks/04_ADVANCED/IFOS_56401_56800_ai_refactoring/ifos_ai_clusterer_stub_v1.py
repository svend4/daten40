# ifos_ai_clusterer_stub_v1.py
from __future__ import annotations
from typing import List, Dict

def build_clusters(function_cards: List[Dict], graph_edges: List[Dict]) -> List[Dict]:
    # Placeholder: return one dummy cluster
    return [{
        "cluster_id": "clu.demo",
        "name": "Demo cluster",
        "job_story": "When I do X, I want Y.",
        "members": [c.get("id") for c in function_cards[:5]],
        "recommended_macros": [],
        "version": "1.0.0",
    }]
