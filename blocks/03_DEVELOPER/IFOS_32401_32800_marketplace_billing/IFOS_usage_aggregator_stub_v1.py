# IFOS Usage Aggregator Stub v1
from __future__ import annotations
from typing import Dict, Any, List, Tuple

def aggregate_usage(events: List[Dict[str, Any]]) -> Dict[Tuple[str,str], float]:
    # key: (entitlement_id, meter_id) -> sum(amount)
    totals={}
    seen=set()
    for ev in events:
        key=ev.get("idempotency_key")
        if key in seen:
            continue
        seen.add(key)
        k=(ev["entitlement_id"], ev["meter_id"])
        totals[k]=totals.get(k, 0.0) + float(ev.get("amount",0))
    return totals
