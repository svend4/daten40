# IFOS SLO Evaluator Stub v1
from __future__ import annotations
from typing import Dict, Any

def evaluate(slo: Dict[str, Any], observed: Dict[str, Any]) -> Dict[str, Any]:
    # observed contains aggregated metrics for window: success_rate, latency_p95_ms, etc.
    ok = True
    failed = []
    for obj in slo.get("objectives", []) or []:
        name = obj.get("name")
        thr = float(obj.get("threshold", 0))
        cmp = obj.get("comparison")
        val = float(observed.get(name, 0))
        if cmp == ">=" and not (val >= thr):
            ok = False; failed.append({"name": name, "val": val, "thr": thr})
        if cmp == "<=" and not (val <= thr):
            ok = False; failed.append({"name": name, "val": val, "thr": thr})
    return {"ok": ok, "failed": failed}
