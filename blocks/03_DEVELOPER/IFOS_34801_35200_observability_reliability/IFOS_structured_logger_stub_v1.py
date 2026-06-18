# IFOS Structured Logger Stub v1
from __future__ import annotations
from typing import Dict, Any
import json, datetime, uuid

def log(level: str, message: str, tenant_id: str, meta: Dict[str, Any] | None=None) -> Dict[str, Any]:
    ev={
        "event_id": "log."+uuid.uuid4().hex[:12],
        "ts": datetime.datetime.utcnow().isoformat()+"Z",
        "level": level,
        "message": message,
        "tenant_id": tenant_id,
        "meta": meta or {},
        "version":"1.0.0"
    }
    return ev
