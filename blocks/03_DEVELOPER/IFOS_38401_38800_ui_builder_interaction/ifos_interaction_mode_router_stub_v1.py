# ifos_interaction_mode_router_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def route(mode: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
    if mode.get("name") in ("assisted","auto") and action.get("risk") == "confirm":
        return {"decision":"require_approval"}
    return {"decision":"allow"}
