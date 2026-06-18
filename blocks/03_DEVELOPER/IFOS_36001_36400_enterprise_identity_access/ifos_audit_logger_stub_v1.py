# ifos_audit_logger_stub_v1.py
from __future__ import annotations
from typing import Dict, Any
import datetime, uuid

def audit(action: str, tenant_id: str, actor: Dict[str, Any], resource: Dict[str, Any], result: str="ok") -> Dict[str, Any]:
    return {
        "audit_id":"aud."+uuid.uuid4().hex[:12],
        "tenant_id":tenant_id,
        "ts":datetime.datetime.utcnow().isoformat()+"Z",
        "actor":actor,
        "action":action,
        "resource":resource,
        "result":result,
        "version":"1.0.0"
    }
