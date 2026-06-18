# ifos_cost_aggregator_stub_v1.py
from __future__ import annotations
from typing import List, Dict

def aggregate(cost_events: List[Dict]) -> Dict:
    total=sum(e.get("amount",0) for e in cost_events)
    return {"total": total}
