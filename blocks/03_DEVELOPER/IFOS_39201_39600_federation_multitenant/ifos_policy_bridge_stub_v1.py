# ifos_policy_bridge_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def bridge(provider_policies: Dict[str, Any], consumer_policies: Dict[str, Any]) -> Dict[str, Any]:
    """Return OK/WARN/BLOCK based on minimal compatibility rules."""
    if provider_policies.get("dlp") == "block" and consumer_policies.get("dlp") != "block":
        return {"status":"BLOCK","reason":"consumer must enable dlp=block"}
    if provider_policies.get("export_mask_pii") and not consumer_policies.get("export_mask_pii"):
        return {"status":"WARN","reason":"consumer should enable export_mask_pii"}
    return {"status":"OK"}
