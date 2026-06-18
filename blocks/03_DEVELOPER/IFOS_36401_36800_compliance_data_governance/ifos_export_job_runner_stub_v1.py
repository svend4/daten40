# ifos_export_job_runner_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def run_export(job: Dict[str, Any]) -> Dict[str, Any]:
    j=dict(job)
    j["status"]="done"
    j["result_ref"]="exports/"+j["export_id"]+".zip"
    return j
