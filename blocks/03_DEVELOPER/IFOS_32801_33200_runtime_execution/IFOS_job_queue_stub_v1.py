# IFOS Job Queue Stub v1
from __future__ import annotations
from typing import Dict, Any, List

class JobQueue:
    def __init__(self) -> None:
        self.jobs: List[Dict[str, Any]] = []

    def enqueue(self, job: Dict[str, Any]) -> None:
        self.jobs.append(job)

    def dequeue(self) -> Dict[str, Any] | None:
        if not self.jobs:
            return None
        return self.jobs.pop(0)
