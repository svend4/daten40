# IFOS Metrics Collector Stub v1
from __future__ import annotations
from typing import Dict, Any, List
import datetime, uuid

STORE: List[Dict[str, Any]]=[]

def emit(name: str, kind: str, value: float, tags: Dict[str, str]) -> Dict[str, Any]:
    m={
        "metric_id":"m."+uuid.uuid4().hex[:12],
        "name":name,
        "kind":kind,
        "value":float(value),
        "ts":datetime.datetime.utcnow().isoformat()+"Z",
        "tags":tags,
        "version":"1.0.0"
    }
    STORE.append(m)
    return m
