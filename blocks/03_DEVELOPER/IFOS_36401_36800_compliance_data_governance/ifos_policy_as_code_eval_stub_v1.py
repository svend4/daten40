# ifos_policy_as_code_eval_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List

def eval_rules(rules: List[Dict[str, Any]], phase: str, ctx: Dict[str, Any]) -> str:
    # Evaluate by priority (lower is higher priority)
    cand=[r for r in rules if r.get("phase")==phase]
    cand.sort(key=lambda r: r.get("priority", 9999))
    for r in cand:
        cond=r.get("condition", {})
        # very small matcher: equality checks
        ok=True
        for k,v in cond.items():
            if ctx.get(k)!=v:
                ok=False
                break
        if ok:
            return r.get("effect","allow")
    return "allow"
