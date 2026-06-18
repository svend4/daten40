# IFOS Audit Logger Stub v1
from __future__ import annotations
from typing import Dict, Any, List
import time

class AuditLog:
    def __init__(self):
        self.events: List[Dict[str, Any]] = []
    def append(self, event: Dict[str, Any]) -> None:
        self.events.append(event)

def make_event(workspace_id: str, actor: Dict[str, Any], action: str, resource: Dict[str, Any], outcome: str, context: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "event_id": f"ae.{int(time.time()*1000)}",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "workspace_id": workspace_id,
        "actor": actor,
        "action": action,
        "resource": resource,
        "outcome": outcome,
        "context": context,
        "version":"1.0.0",
    }
