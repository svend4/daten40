# ifos_incident_manager_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def open_incident(title: str, impacted: list[str]) -> Dict[str, Any]:
    return {"title": title, "status":"investigating", "impacted": impacted, "timeline":[]}
