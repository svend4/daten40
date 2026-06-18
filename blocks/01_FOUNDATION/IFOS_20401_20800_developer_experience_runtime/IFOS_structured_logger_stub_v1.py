# IFOS Structured Logger Stub v1
from __future__ import annotations
from typing import Dict, Any
import json, time

def log(level: str, correlation_id: str, job_id: str, step_id: str, message: str, fields: Dict[str, Any]) -> str:
    event = {
        "at": time.time(),
        "level": level,
        "correlation_id": correlation_id,
        "job_id": job_id,
        "step_id": step_id,
        "message": message,
        "fields": fields,
    }
    return json.dumps(event, ensure_ascii=False)
