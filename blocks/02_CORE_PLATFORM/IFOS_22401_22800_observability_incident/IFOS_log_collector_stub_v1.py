# IFOS Log Collector Stub v1
from __future__ import annotations
from typing import Dict, Any, List
import re

def apply_redaction(event: Dict[str, Any], rules: List[Dict[str, Any]]) -> Dict[str, Any]:
    msg = event.get("message","")
    data = event.get("data",{})
    for r in rules:
        pat=re.compile(r["pattern"])
        if r.get("scope") in ("logs","both"):
            msg = pat.sub(r["replacement"], msg)
        if r.get("scope") in ("logs","both"):
            # naive redaction for string values in data
            for k,v in list(data.items()):
                if isinstance(v,str):
                    data[k]=pat.sub(r["replacement"], v)
    event["message"]=msg
    event["data"]=data
    return event

def ingest(events: List[Dict[str, Any]]) -> int:
    # Stub: write to storage
    return len(events)
