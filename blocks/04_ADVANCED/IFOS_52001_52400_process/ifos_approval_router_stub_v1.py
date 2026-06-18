# ifos_approval_router_stub_v1.py
from __future__ import annotations
from typing import Dict

def route(ctx: Dict) -> str:
    amount=float(ctx.get("amount",0))
    if amount>500: return "manager+finance"
    return "manager"
