# IFOS Fallback Orchestrator Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def decide(policy: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
    actions=[]
    for s in policy.get("strategies", []):
        when=s.get("when","")
        # Stub: simple string matching
        if "burn_rate" in when and context.get("burn_rate",0) > 2.0:
            actions += s.get("then", [])
        if "delivery_success_ratio" in when and context.get("delivery_success_ratio",1) < 0.85:
            actions += s.get("then", [])
    return actions
