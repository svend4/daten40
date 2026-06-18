# ifos_make_n8n_bridge_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def trigger_make(webhook_url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    # Stub: would HTTP POST in real implementation.
    return {"status":"queued","run_url": None}
