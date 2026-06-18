# IFOS Approval Router Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def route(flow: Dict[str, Any], request: Dict[str, Any]) -> List[Dict[str, Any]]:
    steps=[]
    target=request.get("target", {})
    for s in flow.get("steps", []):
        cond=s.get("conditions") or {}
        ok=True
        # simple checks
        if "risk" in cond and target.get("risk") != cond["risk"]:
            ok=False
        if "cost_over" in cond and float(target.get("cost_estimate",0)) <= float(cond["cost_over"]):
            ok=False
        if ok:
            steps.append(s)
    if not steps:
        steps=[{"kind":"auto","assignee":"system","conditions":{}}]
    return steps
