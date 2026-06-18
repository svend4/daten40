# ifos_retention_enforcer_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List
import datetime

def should_delete(created_at: datetime.datetime, ttl_days: int) -> bool:
    if ttl_days <= 0:
        return True
    return (datetime.datetime.utcnow() - created_at).days >= ttl_days

def apply_retention(items: List[Dict[str, Any]], rule: Dict[str, Any], legal_hold_ids: set[str]) -> List[Dict[str, Any]]:
    # items: {id, created_at, data_class, hold_id?}
    kept=[]
    ttl=rule.get("ttl_days", 0)
    for it in items:
        if it.get("hold_id") in legal_hold_ids:
            kept.append(it)
            continue
        if should_delete(it["created_at"], ttl):
            continue
        kept.append(it)
    return kept
