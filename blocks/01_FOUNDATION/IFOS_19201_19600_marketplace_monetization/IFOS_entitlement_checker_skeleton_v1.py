# IFOS Entitlement Checker Skeleton v1
from __future__ import annotations
from typing import Dict, Any

def check(entitlement: Dict[str, Any], action: str, usage: Dict[str, Any]) -> Dict[str, Any]:
    # usage can include runs_today, connectors_used, etc.
    limits = entitlement.get("limits", {})
    if action == "run":
        max_runs = int(limits.get("runs_per_day", 0))
        if max_runs and int(usage.get("runs_today", 0)) >= max_runs:
            return {"allowed": False, "reason": "limit.runs_per_day"}
    return {"allowed": True}
