# ifos_policy_evaluator_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def evaluate(context: Dict, rules: List[Dict]) -> Dict:
    # Placeholder evaluator returning allow by default.
    return {"outcome": "allow", "actions": [], "reason": "no matching rules"}
