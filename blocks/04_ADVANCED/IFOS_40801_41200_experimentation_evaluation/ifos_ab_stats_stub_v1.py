# ifos_ab_stats_stub_v1.py
from __future__ import annotations
from typing import Dict

def delta(a: Dict[str, float], b: Dict[str, float], metric: str) -> float:
    return float(b.get(metric,0.0) - a.get(metric,0.0))
