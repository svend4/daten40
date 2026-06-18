# ifos_ui_router_stub_v1.py
from __future__ import annotations
from typing import Dict

def switch_mode(state: Dict, mode: str) -> Dict:
    state["mode"]=mode
    return state
