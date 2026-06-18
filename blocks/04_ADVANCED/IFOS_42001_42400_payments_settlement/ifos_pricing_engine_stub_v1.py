# ifos_pricing_engine_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def price(model: Dict[str, Any], usage_units: int) -> Dict[str, float]:
    fixed=float(model.get("fixed_amount") or 0.0)
    usage=model.get("usage") or {}
    rate=float(usage.get("rate") or 0.0)
    free=int(usage.get("free_units") or 0)
    bill=max(0, usage_units-free)
    return {"fixed": fixed, "usage": bill*rate, "total": fixed + bill*rate}
