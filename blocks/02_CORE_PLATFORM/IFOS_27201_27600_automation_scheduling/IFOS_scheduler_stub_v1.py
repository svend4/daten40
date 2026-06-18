# IFOS Scheduler Stub v1
from __future__ import annotations
from typing import Dict, Any, List
import time, hashlib, json

def compute_idempotency_key(job_id: str, bindings: Dict[str, Any], window: str) -> str:
    payload = {"job_id": job_id, "bindings": bindings, "window": window}
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def should_run(idempotency_store: Dict[str, Any], key: str) -> bool:
    return key not in idempotency_store

def mark_done(idempotency_store: Dict[str, Any], key: str, result_ref: str = "") -> None:
    idempotency_store[key] = {"status":"done","result_ref":result_ref,"ts":time.time()}
