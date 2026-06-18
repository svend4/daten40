# IFOS Policy Evaluator Stub v1
from __future__ import annotations
from typing import Dict, Any

class PolicyEvaluator:
    def __init__(self, policy: Dict[str, Any]) -> None:
        self.policy = policy

    def evaluate(self, req: Dict[str, Any]) -> Dict[str, Any]:
        # Minimal: deny if input requests forbidden op
        inputs=req.get("inputs", {})
        if inputs.get("op") == "port_scan":
            return {"allowed": False, "reason": "dangerous_op denied"}
        return {"allowed": True, "reason": None}
