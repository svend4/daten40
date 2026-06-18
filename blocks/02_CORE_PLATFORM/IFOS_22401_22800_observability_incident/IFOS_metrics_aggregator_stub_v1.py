# IFOS Metrics Aggregator Stub v1
from __future__ import annotations
from typing import Dict, Any, List, Tuple

def aggregate(points: List[Dict[str, Any]]) -> Dict[str, float]:
    # Stub: returns latest value per metric name
    latest={}
    for p in points:
        latest[p["name"]] = float(p["value"])
    return latest
