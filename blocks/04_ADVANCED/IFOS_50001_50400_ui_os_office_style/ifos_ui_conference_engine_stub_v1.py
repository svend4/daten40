# ifos_ui_conference_engine_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def run(topic: str, inputs: List[Dict]) -> Dict:
    return {"topic":topic,"clusters":[], "outputs":[{"type":"protocol","format":"md"}]}
