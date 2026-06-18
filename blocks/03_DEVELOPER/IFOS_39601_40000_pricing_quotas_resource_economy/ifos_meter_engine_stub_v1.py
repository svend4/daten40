# ifos_meter_engine_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List

def price_event(event: Dict[str, Any], plan: Dict[str, Any]) -> float:
    price_map={p["resource_id"]: p["price_per_unit"] for p in plan.get("prices", [])}
    total=0.0
    for r in event.get("resources", []):
        total += float(r.get("quantity",0)) * float(price_map.get(r.get("resource_id"), 0.0))
    return total
