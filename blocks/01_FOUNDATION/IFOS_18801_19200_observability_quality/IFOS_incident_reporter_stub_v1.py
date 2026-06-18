# IFOS Incident Reporter Stub v1
from __future__ import annotations
from typing import Dict, Any
import time

def open_incident(title: str, severity: str, impact: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "incident_id": "inc.generated",
        "title": title,
        "status": "open",
        "severity": severity,
        "timeline": [{"at": time.time(), "event": "opened"}],
        "impact": impact,
        "root_cause": "",
        "actions_taken": [],
        "prevention": [],
        "links": [],
        "version": "1.0.0",
        "updated_at": ""
    }
