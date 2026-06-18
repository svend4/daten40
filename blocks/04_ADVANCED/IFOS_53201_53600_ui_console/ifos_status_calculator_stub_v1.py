# ifos_status_calculator_stub_v1.py
from __future__ import annotations
from typing import Dict

def calc(obj: Dict) -> Dict:
    # trivial placeholder
    if obj.get("error") == "auth":
        return {"status":"auth_required","next_actions":["re-auth"],"meaning":"Authorization required"}
    return {"status":"ok","next_actions":[],"meaning":"Healthy"}
