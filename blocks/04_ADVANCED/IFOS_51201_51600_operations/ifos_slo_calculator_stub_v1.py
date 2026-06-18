# ifos_slo_calculator_stub_v1.py
from __future__ import annotations
from typing import Dict

def burn_rate(errors: int, total: int, slo: float) -> float:
    if total <= 0: return 0.0
    err_rate = errors/total
    allowed = 1.0 - slo
    return (err_rate/allowed) if allowed>0 else 0.0
