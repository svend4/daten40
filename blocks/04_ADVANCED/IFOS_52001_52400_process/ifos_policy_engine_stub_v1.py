# ifos_policy_engine_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def evaluate(policy: Dict[str,Any], ctx: Dict[str,Any]) -> Dict[str,Any]:
    # minimal evaluator for (field, op, value)
    w=policy.get("when",{})
    field=w.get("field"); op=w.get("op"); val=w.get("value")
    cur=ctx.get(field)
    ok=False
    if op==">" and cur is not None: ok = cur > val
    if op=="==" and cur is not None: ok = cur == val
    return {"matched": ok, "then": policy.get("then") if ok else None}
