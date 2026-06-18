# ifos_ui_command_builder_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def build(intent: str, terms: List[str], target: str, params: Dict) -> Dict:
    return {"intent":intent,"terms":terms,"target":target,"params":params}
