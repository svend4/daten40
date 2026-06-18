# ifos_abac_engine_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List

def evaluate(policies: List[Dict[str, Any]], user: Dict[str, Any], resource: Dict[str, Any], context: Dict[str, Any]) -> str:
    # Very simplified: deny if any deny-policy matches a simple tag check.
    for p in policies:
        if p.get("effect")=="deny":
            for rule in p.get("rules", []):
                cond=rule.get("if", {})
                if cond.get("resource.tags")=="risky" and "risky" in resource.get("tags", []):
                    return "deny"
    return "allow"
