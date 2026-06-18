# IFOS Policy Engine Stub v1
from __future__ import annotations
from typing import Dict, Any, List, Tuple

def eval_policy(policies: List[Dict[str, Any]], ctx: Dict[str, Any]) -> Tuple[bool, List[str]]:
    violations=[]
    for p in policies:
        if not p.get("enabled", True):
            continue
        for rule in p.get("rules", []):
            k=rule.get("kind")
            if k=="license_deny":
                if ctx.get("license") in set(rule.get("deny", [])):
                    violations.append(f"license denied: {ctx.get('license')}")
            if k=="data_residency":
                allowed=set(rule.get("allow", []))
                if ctx.get("data_residency") not in allowed:
                    violations.append("data residency violation")
            if k=="network_outbound_deny":
                if ctx.get("network_outbound", False):
                    violations.append("outbound network denied")
    return (len(violations)==0, violations)
