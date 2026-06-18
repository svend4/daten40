# IFOS Observability Stub v1
from __future__ import annotations
from typing import Dict, Any, List

class Obs:
    def __init__(self):
        self.logs: List[Dict[str, Any]] = []
        self.metrics: List[Dict[str, Any]] = []

    def log(self, job_id: str, level: str, message: str, context: Dict[str, Any] | None = None) -> None:
        self.logs.append({"job_id":job_id,"level":level,"message":message,"context":context or {}})

    def metric(self, job_id: str, name: str, value: float, unit: str="") -> None:
        self.metrics.append({"job_id":job_id,"name":name,"value":value,"unit":unit})
