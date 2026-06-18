# IFOS Retention Manager Stub v1
from __future__ import annotations
from typing import Dict, Any, List
import datetime

def apply_retention(items: List[Dict[str, Any]], policy: Dict[str, Any], now: datetime.datetime | None=None) -> Dict[str, Any]:
    """Stub: returns counts for move/delete decisions."""
    now = now or datetime.datetime.utcnow()
    return {"checked": len(items), "moved": 0, "deleted": 0, "policy_id": policy.get("policy_id","")}
