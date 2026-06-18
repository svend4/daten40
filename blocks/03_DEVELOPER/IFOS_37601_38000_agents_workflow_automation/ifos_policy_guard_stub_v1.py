# ifos_policy_guard_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, Tuple

def check(policy: Dict[str, Any], tool: Dict[str, Any]) -> Tuple[str, str]:
    # returns (decision, reason): allow / deny / require_approval
    for rule in policy.get("rules", []):
        tm=rule.get("tool_match") or {}
        if "risk" in tm and tm["risk"] == tool.get("risk"):
            return rule["effect"], rule.get("notes","")
        if "name_prefix" in tm and tool.get("name","").startswith(tm["name_prefix"]):
            return rule["effect"], rule.get("notes","")
    return "allow", "default allow"
