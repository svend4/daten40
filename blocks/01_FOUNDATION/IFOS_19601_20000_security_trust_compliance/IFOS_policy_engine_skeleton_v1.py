# IFOS Policy Engine Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List, Tuple

def decide(policy: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    # Very simplified evaluator: checks precomputed flags in context
    decision = policy.get("enforcement", {}).get("default", "allow")
    reasons: List[str] = []
    # Example: deny on critical
    crit = int(context.get("scan_summary", {}).get("critical", 0))
    if crit > 0:
        return {"decision": "deny", "reasons": ["critical vulnerabilities present"]}
    # Warn on high/medium counts
    high = int(context.get("scan_summary", {}).get("high", 0))
    med = int(context.get("scan_summary", {}).get("medium", 0))
    if high > 0 or med > 0:
        decision = "warn"
        reasons.append("vulnerabilities present")
    if not bool(context.get("signature_verified", False)):
        return {"decision": "deny", "reasons": ["signature not verified"]}
    return {"decision": decision, "reasons": reasons}
