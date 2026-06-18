# ifos_local_runtime_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def run_bundle(bundle_id: str, profile: Dict[str, Any]) -> Dict[str, Any]:
    return {"bundle_id":bundle_id, "profile":profile.get("name"), "status":"ok"}
