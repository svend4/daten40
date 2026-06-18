# IFOS News Conference Compiler Stub v1
from __future__ import annotations
from typing import Dict, Any, List
from collections import defaultdict

def dedupe(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out = []
    for it in items:
        key = (it.get("url") or it.get("title","")).strip().lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
    return out

def cluster_by_topic(items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    clusters = defaultdict(list)
    for it in items:
        topic = (it.get("topic") or "general")
        clusters[topic].append(it)
    return dict(clusters)

def build(conference: Dict[str, Any], items: List[Dict[str, Any]]) -> Dict[str, Any]:
    if conference.get("pipeline",{}).get("dedupe"):
        items = dedupe(items)
    clusters = cluster_by_topic(items) if conference.get("pipeline",{}).get("cluster") else {"all": items}
    agenda = []
    for a in conference.get("agenda",[]) or []:
        topic = a.get("topic")
        top_n = int(a.get("top_n",5))
        top_items = (clusters.get(topic, [])[:top_n])
        agenda.append({"topic": topic, "items": top_items})
    return {"conf_id": conference.get("conf_id"), "agenda": agenda}
