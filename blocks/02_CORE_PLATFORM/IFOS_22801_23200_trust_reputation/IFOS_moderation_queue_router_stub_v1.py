# IFOS Moderation Queue Router Stub v1
from __future__ import annotations
from typing import Dict, Any

def route(item: Dict[str, Any]) -> str:
    # Route based on severity and fraud label
    if item.get("label") == "fraud_likely":
        return "queue://security_high"
    if item.get("label") == "suspicious":
        return "queue://moderation"
    return "queue://auto_approve"
