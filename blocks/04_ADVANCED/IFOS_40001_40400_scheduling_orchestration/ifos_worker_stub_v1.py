# ifos_worker_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def run_job(job: Dict[str, Any]) -> Dict[str, Any]:
    # Stub: pretend success
    return {"job_id": job["job_id"], "status": "succeeded"}
