# IFOS Autofix Engine Stub v1
from __future__ import annotations
from typing import Dict, Any

def plan_from_diagnosis(target: Dict[str, Any], diagnosis: Dict[str, Any]) -> Dict[str, Any]:
    steps = []
    risk = "low"
    requires_approval = True
    for c in diagnosis.get("probable_causes", []) or []:
        if c.get("code") == "E_SECRET_MISSING":
            steps.append({"kind":"create_secret_ref","description":"Create missing secret_ref (no value)"})
            steps.append({"kind":"update_config","description":"Bind secret_ref in job config"})
    if not steps:
        risk = "medium"
        steps.append({"kind":"other","description":"No safe autofix steps found; suggest manual triage"})
    return {"risk": risk, "steps": steps, "requires_approval": requires_approval}
