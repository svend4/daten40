# IFOS Dedupe Engine Stub v1
from __future__ import annotations
from typing import Dict, Any, List
import hashlib

def canonical_id(record: Dict[str, Any]) -> str:
    url = (record.get("canonical_url") or "").strip().lower().encode("utf-8")
    return "can_" + hashlib.sha1(url).hexdigest()  # deterministic

def dedupe(records: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    clusters = {}
    for r in records:
        cid = canonical_id(r)
        clusters.setdefault(cid, []).append(r)
    return clusters
