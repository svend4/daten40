# ifos_cost_guard_stub_v1.py
from __future__ import annotations
from typing import Dict

def should_enter_safe_mode(cost_now: float, budget: Dict) -> bool:
    return cost_now >= float(budget.get("limit",0))*0.9
