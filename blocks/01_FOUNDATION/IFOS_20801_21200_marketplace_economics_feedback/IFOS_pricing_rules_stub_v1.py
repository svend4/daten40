# IFOS Pricing Rules Stub v1
from __future__ import annotations
from typing import Dict, Any

def estimate_cost(plan: Dict[str, Any], usage: Dict[str, Any]) -> float:
    model = plan.get("model")
    prices = plan.get("prices", {})
    if model == "usage_based":
        per_run = float(prices.get("per_run", 0.0))
        runs = float(usage.get("runs", 0))
        return per_run * runs
    if model == "subscription":
        return float(prices.get("monthly", 0.0))
    return 0.0
