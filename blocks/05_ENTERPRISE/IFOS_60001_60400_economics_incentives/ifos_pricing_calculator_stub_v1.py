# ifos_pricing_calculator_stub_v1.py
from __future__ import annotations
from typing import Dict

def calc_usage(cost_units: float, price_per_unit: float) -> float:
    return float(cost_units) * float(price_per_unit)
