# IFOS Alert Evaluator Stub v1
from __future__ import annotations
from typing import Dict, Any

def eval_alert(expr: str, ctx: Dict[str, Any]) -> bool:
    # Very simplified evaluator; replace with proper expression engine.
    # Example: "run.success_rate < 0.95"
    try:
        left, op, right = expr.split()[:3]
        val=float(ctx.get(left, 0))
        thr=float(right)
        if op=="<": return val < thr
        if op==">": return val > thr
        return False
    except Exception:
        return False
