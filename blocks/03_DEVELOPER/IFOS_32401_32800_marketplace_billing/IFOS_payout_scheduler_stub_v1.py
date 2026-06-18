# IFOS Payout Scheduler Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def compute_payout(amount_gross: float, platform_cut: float, adjustments: Dict[str, float]) -> float:
    net = amount_gross * (1.0 - platform_cut)
    net += adjustments.get("refunds", 0.0)
    net += adjustments.get("fees", 0.0)
    return round(max(0.0, net), 2)

def schedule_payout(seller_id: str, orders: List[Dict[str, Any]], platform_cut: float = 0.2) -> Dict[str, Any]:
    gross=sum(float(o.get("amount_total",0.0)) for o in orders)
    net=compute_payout(gross, platform_cut, {"refunds":0.0,"fees":0.0})
    return {"seller_id":seller_id,"gross":gross,"net":net,"status":"scheduled"}
