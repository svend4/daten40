# IFOS A/B Router Stub v1
from __future__ import annotations
from typing import Dict, Any
import hashlib

def pick_variant(test: Dict[str, Any], user_id: str) -> str:
    variants=test.get("variants", [])
    if not variants:
        return "A"
    h=int(hashlib.sha256(user_id.encode("utf-8")).hexdigest(), 16)
    r=(h % 10000)/10000.0
    acc=0.0
    for v in variants:
        acc += float(v.get("traffic",0.0))
        if r <= acc:
            return v["id"]
    return variants[-1]["id"]
