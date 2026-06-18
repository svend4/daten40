# IFOS Policy Engine Stub v1
from __future__ import annotations
from typing import Dict, Any

def evaluate(policy: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
    # action: {"actor_role":"Editor","action":"install","network.domains":["api.telegram.org"]}
    # naive allowlist/denylist evaluation
    for rule in policy.get("rules", []) or []:
        effect = rule.get("effect")
        match = rule.get("match", {})
        # very simplified: domain allow list check
        if "network.domains" in match:
            allowed = match["network.domains"]
            if allowed == "*":
                if effect == "deny":
                    return {"allowed": False, "reason": "Denied by deny_unknown_domains", "requires_approval": False}
            else:
                req = action.get("network.domains", [])
                if any(d in allowed for d in req):
                    if effect == "allow":
                        return {"allowed": True, "reason": "Allowed by allow_telegram_api", "requires_approval": rule.get("requires_approval", False)}
    return {"allowed": False, "reason": "No matching allow rule", "requires_approval": False}
