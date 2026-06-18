# ifos_secret_policy_eval_stub_v1.py
from __future__ import annotations
from typing import Dict, Tuple

def evaluate(policy: Dict, request: Dict) -> Tuple[bool,str]:
    if request.get("export") is True:
        return False, "deny_export"
    return True, "allowed"
