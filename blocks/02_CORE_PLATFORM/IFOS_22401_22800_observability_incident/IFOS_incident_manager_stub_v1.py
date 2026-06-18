# IFOS Incident Manager Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def declare(title: str, severity: str, affected: List[str], owner: str, links: Dict[str, str]) -> Dict[str, Any]:
    return {
        "incident_id":"inc.demo",
        "title":title,
        "severity":severity,
        "status":"open",
        "affected":affected,
        "owner":owner,
        "links":links
    }

def add_timeline_entry(timeline: Dict[str, Any], ts: str, kind: str, text: str, ref: str="") -> None:
    timeline.setdefault("entries", []).append({"ts":ts,"type":kind,"text":text,"ref":ref})
