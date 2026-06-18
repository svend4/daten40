# ifos_digest_builder_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def build_digest(clusters: List[Dict], max_clusters:int=10) -> Dict:
    top=clusters[:max_clusters]
    return {"title":"Digest", "clusters":top, "conclusions":["focus on top items"], "actions":[]}
