# ifos_story_clusterer_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def cluster(items: List[Dict], threshold: float=0.86) -> List[Dict]:
    # stub: naive clustering by 'topic_key'
    clusters={}
    for it in items:
        key=it.get("topic_key","misc")
        clusters.setdefault(key, []).append(it)
    out=[]
    for k, lst in clusters.items():
        out.append({"cluster_id":"cl."+k, "canonical_title": lst[0].get("title",""), "sources":[x.get("source") for x in lst]})
    return out
