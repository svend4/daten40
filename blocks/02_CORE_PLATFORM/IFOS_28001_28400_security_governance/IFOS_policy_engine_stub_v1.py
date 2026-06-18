# IFOS Policy Engine Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def evaluate(policies: List[Dict[str, Any]], actor: Dict[str, Any], action: str, resource: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Very small demo: returns decision allow/deny/require with measures."""
    decision = {"effect":"allow","measures":[],"matched":None}
    for pol in policies:
        if not pol.get("enabled", True):
            continue
        if action not in (pol.get("actions") or []):
            continue
        # naive resource match: '*' allowed
        res_patterns = pol.get("resources") or []
        if not any(pat=="*" or pat.startswith(resource.get("kind","")+"*") for pat in res_patterns):
            continue
        decision["effect"] = pol.get("effect","allow")
        decision["measures"] = pol.get("enforced_measures") or []
        decision["matched"] = pol.get("policy_id")
        # deny has priority
        if decision["effect"] == "deny":
            return decision
    return decision
