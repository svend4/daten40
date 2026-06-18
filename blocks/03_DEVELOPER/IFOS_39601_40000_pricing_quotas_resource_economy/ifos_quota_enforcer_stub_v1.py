# ifos_quota_enforcer_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def check(usage: Dict[str, float], quota: Dict[str, Any]) -> Dict[str, Any]:
    for lim in quota.get("limits", []):
        rid=lim["resource_id"]
        maxv=float(lim["max"])
        cur=float(usage.get(rid, 0.0))
        if cur > maxv:
            return {"allowed": False, "on_exceed": quota.get("on_exceed","block"), "resource_id": rid, "current": cur, "max": maxv}
    return {"allowed": True}
