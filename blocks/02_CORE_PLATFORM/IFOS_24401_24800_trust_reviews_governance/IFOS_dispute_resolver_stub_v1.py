# IFOS Dispute Resolver Stub v1
from __future__ import annotations
from typing import Dict, Any

def triage_dispute(case: Dict[str, Any]) -> Dict[str, Any]:
    claim = case.get("claim","").lower()
    if "снять карантин" in claim or "remove quarantine" in claim:
        case["status"]="needs_info"
        case.setdefault("timeline", []).append({"event":"needs_info","note":"request receipts & scope list"})
    else:
        case["status"]="triage"
    return case
