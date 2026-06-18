# IFOS Scheduler Stub v1
from __future__ import annotations
from typing import Dict, Any, List

class Scheduler:
    def __init__(self):
        self.jobs: List[Dict[str, Any]] = []

    def add(self, sched_job: Dict[str, Any]) -> None:
        self.jobs.append(sched_job)

    def list(self) -> List[Dict[str, Any]]:
        return self.jobs
