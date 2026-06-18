# ifos_publish_pipeline_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def run_publish(job: Dict[str, Any]) -> Dict[str, Any]:
    for step in job.get("steps", []):
        step["status"]="done"
    job["status"]="succeeded"
    return job
