# IFOS Coupon Engine Stub v1
from __future__ import annotations
from typing import Dict, Any
import datetime

def is_coupon_valid(c: Dict[str, Any], now: str | None = None) -> bool:
    if not c.get("active"):
        return False
    # ignore date windows for stub
    return True

def redeem(c: Dict[str, Any]) -> Dict[str, Any]:
    # decrement max_redemptions if set
    mr=c.get("max_redemptions")
    if mr is None:
        return c
    c["max_redemptions"]=max(0, int(mr)-1)
    if c["max_redemptions"]==0:
        c["active"]=False
    return c
