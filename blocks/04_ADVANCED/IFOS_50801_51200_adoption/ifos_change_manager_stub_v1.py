# ifos_change_manager_stub_v1.py
from __future__ import annotations
from typing import Dict

def approve(ticket: Dict, approver: str) -> Dict:
    ticket["approved_by"]=approver
    return ticket
