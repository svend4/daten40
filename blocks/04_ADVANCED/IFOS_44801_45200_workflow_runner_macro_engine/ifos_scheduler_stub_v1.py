# ifos_scheduler_stub_v1.py
from __future__ import annotations
from typing import Dict

def register(schedule: Dict) -> Dict:
    return {"status":"registered","schedule_id":schedule["schedule_id"]}
