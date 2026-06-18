# ifos_training_scheduler_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def schedule(modules: List[Dict], calendar: Dict) -> Dict:
    return {"scheduled": len(modules), "calendar": calendar}
