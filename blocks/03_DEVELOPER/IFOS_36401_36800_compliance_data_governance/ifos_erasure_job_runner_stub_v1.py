# ifos_erasure_job_runner_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List

def run_erasure(job: Dict[str, Any], holds: List[Dict[str, Any]]) -> Dict[str, Any]:
    j=dict(job)
    # block if any active hold applies
    for h in holds:
        if h.get("status")=="active":
            j["status"]="blocked_legal_hold"
            j["report_ref"]="reports/"+j["erasure_id"]+".json"
            return j
    j["status"]="done"
    j["report_ref"]="reports/"+j["erasure_id"]+".json"
    return j
