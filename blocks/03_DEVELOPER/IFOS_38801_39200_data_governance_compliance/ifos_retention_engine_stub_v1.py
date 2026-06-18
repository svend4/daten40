# ifos_retention_engine_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def next_action(resource: Dict[str, Any], policy: Dict[str, Any]) -> Dict[str, Any]:
    # Stub: returns action based on tag
    for rule in policy.get("rules", []):
        match=rule.get("match", {})
        if match.get("tag") in resource.get("tags", []):
            return {"action": rule.get("action"), "retain_for_days": rule.get("retain_for_days")}
    return {"action":"archive","retain_for_days":365}
