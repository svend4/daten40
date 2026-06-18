# ifos_migration_runner_stub_v1.py
from __future__ import annotations
from typing import Dict

def run(job: Dict) -> Dict:
    return {"job_id": job.get("job_id",""), "status":"dry_run_ok" if job.get("dry_run") else "started"}
