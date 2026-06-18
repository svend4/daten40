# ifos_legal_hold_checker_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List

def is_blocked(resource: Dict[str, Any], holds: List[Dict[str, Any]]) -> bool:
    rid=resource.get("run_id") or resource.get("id")
    for h in holds:
        if h.get("status")!="active":
            continue
        scope=h.get("scope", {})
        if rid and rid in scope.get("run_ids", []):
            return True
    return False
