# ifos_ui_wizard_engine_stub_v1.py
from __future__ import annotations
from typing import Dict

def start(wizard_type: str, bindings: Dict) -> Dict:
    return {"type":wizard_type,"bindings":bindings,"step":"target"}
