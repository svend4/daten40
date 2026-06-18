# IFOS Release Gate Engine Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List

def gate_decision(subject: Dict[str, Any], checks: List[Dict[str, Any]], release_type: str) -> Dict[str, Any]:
    status = "allow"
    for c in checks:
        if c["status"] == "fail":
            status = "block"
            break
        if c["status"] == "warn" and status != "block":
            status = "allow_with_warnings"
    recs = []
    if status != "allow":
        recs.append("Review warnings/failures and rerun smoke+synthetic.")
    return {
        "decision_id": "gate.generated",
        "subject": subject,
        "release_type": release_type,
        "status": status,
        "checks": checks,
        "recommendations": recs,
        "version": "1.0.0",
        "updated_at": ""
    }
