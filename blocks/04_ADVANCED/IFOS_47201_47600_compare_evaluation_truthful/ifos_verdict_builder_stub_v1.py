# ifos_verdict_builder_stub_v1.py
from __future__ import annotations
from typing import Dict

def build(comparison: Dict, confidence: Dict) -> Dict:
    return {"known":[], "likely":[], "uncertain":[], "actions":["check primary source"], "confidence":confidence.get("confidence","low")}
