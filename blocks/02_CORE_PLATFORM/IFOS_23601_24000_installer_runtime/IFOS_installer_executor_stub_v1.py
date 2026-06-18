# IFOS Installer Executor Stub v1
from __future__ import annotations
from typing import Dict, Any

def apply_plan(plan: Dict[str, Any]) -> Dict[str, Any]:
    # Execute steps sequentially (stub). Real impl must be idempotent and safe.
    for step in plan.get("steps", []):
        step["status"] = "completed"
    return {"receipt_id":"rcpt.demo","plan_id":plan.get("plan_id"),"result":"success","lockfile_hash":plan.get("lockfile_hash")}
