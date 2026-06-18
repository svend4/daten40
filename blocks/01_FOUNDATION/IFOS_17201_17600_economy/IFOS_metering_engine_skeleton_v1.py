# IFOS Metering Engine Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List

def aggregate_usage(tenant_id: str, subject: Dict[str, Any], run_records: List[Dict[str, Any]], period_start: str, period_end: str) -> Dict[str, Any]:
    metrics = {"runs":0,"steps":0,"duration_ms":0,"network_bytes":0,"storage_writes":0}
    refs = []
    for r in run_records or []:
        refs.append(r.get("run_id",""))
        metrics["runs"] += 1
        m = r.get("metrics", {}) or {}
        metrics["duration_ms"] += int(m.get("duration_ms",0))
        metrics["steps"] += int(m.get("steps_total",0))
        metrics["network_bytes"] += int(m.get("network_bytes",0))
        # storage_writes can be derived from artifacts (stub)
    return {
        "usage_id":"use.generated",
        "tenant_id":tenant_id,
        "subject":subject,
        "period_start":period_start,
        "period_end":period_end,
        "metrics":metrics,
        "source_run_refs":refs,
        "created_at":"",
    }
