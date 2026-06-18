# IFOS Sandbox Runner Stub v1
from __future__ import annotations
from typing import Dict, Any

def run_in_sandbox(profile: Dict[str, Any], command: Dict[str, Any]) -> Dict[str, Any]:
    # command could be {"kind":"job_run","id":"job.daily_news"}
    return {"status":"ok","sandbox_id": profile.get("sandbox_id"), "result":"executed (stub)"}
