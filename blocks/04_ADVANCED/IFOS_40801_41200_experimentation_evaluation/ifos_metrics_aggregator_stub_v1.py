# ifos_metrics_aggregator_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List

def aggregate(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    total=len(events)
    success=sum(1 for e in events if e.get("name") in ("run_succeeded","install_succeeded"))
    lat=[float(e.get("payload",{}).get("latency_ms",0)) for e in events if "latency_ms" in e.get("payload",{})]
    return {"all_runs": total, "success_runs": success, "success_rate": (success/total if total else 0.0), "latency_avg": (sum(lat)/len(lat) if lat else 0.0)}
