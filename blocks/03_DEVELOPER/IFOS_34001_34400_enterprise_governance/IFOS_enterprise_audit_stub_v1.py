# IFOS Enterprise Audit Stub v1
from __future__ import annotations
from typing import Dict, Any, List
import datetime

AUDIT_LOG: List[Dict[str, Any]]=[]

def append(event: Dict[str, Any]) -> None:
    AUDIT_LOG.append(event)

def list_events(tenant_id: str) -> List[Dict[str, Any]]:
    return [e for e in AUDIT_LOG if e.get("tenant_id")==tenant_id]
