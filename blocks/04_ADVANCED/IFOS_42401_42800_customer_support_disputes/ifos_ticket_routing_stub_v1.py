# ifos_ticket_routing_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List

def route(ticket: Dict[str, Any], queues: List[Dict[str, Any]]) -> str:
    cat=ticket.get("category")
    sev=ticket.get("severity")
    # very small stub: critical/security has priority
    if cat=="security" or sev=="critical":
        return "Security Oncall"
    for q in queues:
        for rule in q.get("routing_rules", []):
            if rule.get("if", {}).get("category")==cat:
                return q.get("name","Default")
    return "Default"
