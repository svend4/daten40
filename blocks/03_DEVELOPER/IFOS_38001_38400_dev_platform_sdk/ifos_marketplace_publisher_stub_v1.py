# ifos_marketplace_publisher_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def publish(plugin: Dict[str, Any], channel: str = "review") -> Dict[str, Any]:
    return {"status":"queued","channel":channel,"plugin":plugin.get("name")}
