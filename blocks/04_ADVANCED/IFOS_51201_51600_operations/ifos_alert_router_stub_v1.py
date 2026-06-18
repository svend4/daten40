# ifos_alert_router_stub_v1.py
from __future__ import annotations
from typing import Dict

def route(alert: Dict) -> str:
    sev = alert.get("severity","low")
    if sev in ("critical","high"): return "oncall"
    return "dashboard"
