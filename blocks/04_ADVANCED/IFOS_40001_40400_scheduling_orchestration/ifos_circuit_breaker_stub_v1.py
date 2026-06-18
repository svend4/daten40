# ifos_circuit_breaker_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def should_trip(metrics: Dict[str, float], threshold_error_rate: float = 0.2) -> bool:
    return float(metrics.get("error_rate",0.0)) >= threshold_error_rate
