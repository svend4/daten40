# IFOS Catalog Miner Stub v1
from __future__ import annotations
from typing import Dict, Any

def register_source(source: Dict[str, Any]) -> str:
    return source["source_id"]

def start_ingest(source_id: str) -> Dict[str, Any]:
    # Stub: create job and enqueue
    return {"job_id":"job.demo","source_id":source_id,"status":"queued"}
