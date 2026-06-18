# IFOS Audit Logger Stub v1
from __future__ import annotations
from typing import Dict, Any, List
import time

AUDIT: List[Dict[str, Any]] = []

def append(record: Dict[str, Any]) -> None:
    AUDIT.append(record)

def log(actor_kind: str, actor_id: str, action: str, subject: Dict[str, Any], result: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    rec = {
        "audit_id": "audit.generated",
        "at": time.time(),
        "actor": {"kind": actor_kind, "id": actor_id},
        "action": action,
        "subject": subject,
        "result": result,
        "metadata": metadata,
        "version": "1.0.0",
        "updated_at": ""
    }
    append(rec)
    return rec
