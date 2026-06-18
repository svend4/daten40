# ifos_cdc_runner_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def start_cdc(spec: Dict[str, Any]) -> Dict[str, Any]:
    return {"cdc_id": spec.get("cdc_id"), "status":"running"}
