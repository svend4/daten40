# ifos_cost_attributor_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def total_cost(cost_model: Dict[str, Any]) -> float:
    return float(sum(c.get("amount",0.0) for c in cost_model.get("components", [])))
