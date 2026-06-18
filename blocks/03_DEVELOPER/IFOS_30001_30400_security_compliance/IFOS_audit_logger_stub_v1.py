# IFOS Audit Logger Stub v1
from __future__ import annotations
from typing import Dict, Any, List

class AuditLog:
    def __init__(self):
        self.events: List[Dict[str, Any]] = []

    def append(self, event: Dict[str, Any]) -> None:
        self.events.append(event)
