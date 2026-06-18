# ifos_backup_runner_stub_v1.py
from __future__ import annotations
from typing import Dict

def run(plan: Dict) -> Dict:
    return {"backup_id": plan.get("backup_id",""), "status":"started"}
