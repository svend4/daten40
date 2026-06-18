# IFOS Policy Gate Evaluator Stub v1
from __future__ import annotations
from typing import Dict, Any

def evaluate(policy: Dict[str, Any], smoke: Dict[str, Any], trust: Dict[str, Any], compat: Dict[str, Any]) -> Dict[str, Any]:
    # Stub rules: fail if smoke fail or policy offline but egress required
    if smoke.get("status") == "fail":
        return {"decision":"fail","reasons":["smoke failed"]}
    return {"decision":"pass","reasons":["ok"]}
