# ifos_sync_engine_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List

def plan(sync_job: Dict[str, Any]) -> List[Dict[str, Any]]:
    include=sync_job.get("scope", {}).get("include", [])
    return [{"action":"pull", "object":obj} for obj in include]
