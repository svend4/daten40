# IFOS Tracer Stub v1
from __future__ import annotations
from typing import Dict, Any
import datetime, uuid

def span(name: str, tenant_id: str, attrs: Dict[str, Any] | None=None) -> Dict[str, Any]:
    t=uuid.uuid4().hex[:12]
    s=uuid.uuid4().hex[:12]
    start=datetime.datetime.utcnow()
    end=start
    return {
        "span_id":"sp."+s,
        "trace_id":"tr."+t,
        "parent_span_id":None,
        "name":name,
        "start_ts":start.isoformat()+"Z",
        "end_ts":end.isoformat()+"Z",
        "status":"ok",
        "tenant_id":tenant_id,
        "attributes":attrs or {},
        "version":"1.0.0"
    }
