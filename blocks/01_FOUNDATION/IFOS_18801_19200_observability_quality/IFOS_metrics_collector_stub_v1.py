# IFOS Metrics Collector Stub v1
from __future__ import annotations
from typing import Dict, Any, List
import time

def emit(metric_name: str, value: float, labels: Dict[str, str]) -> Dict[str, Any]:
    return {"name": metric_name, "value": value, "labels": labels, "at": time.time()}

def ingest_batch(samples: List[Dict[str, Any]]) -> None:
    # Stub: write to TSDB
    pass
