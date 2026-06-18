# IFOS Pricing Engine Stub v1
from __future__ import annotations
from typing import Dict, Any, Optional

def apply_coupon(subtotal: float, coupon: Optional[Dict[str, Any]]) -> float:
    if not coupon or not coupon.get("active"):
        return subtotal
    kind=coupon.get("kind")
    val=float(coupon.get("value",0))
    if kind=="percent":
        return max(0.0, subtotal * (1.0 - val))
    if kind=="fixed":
        return max(0.0, subtotal - val)
    return subtotal

def compute_tax(amount: float, tax_rate: float) -> float:
    return round(amount * tax_rate, 2)

def compute_total(subtotal: float, tax_rate: float, coupon: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
    discounted = apply_coupon(subtotal, coupon)
    tax = compute_tax(discounted, tax_rate)
    total = round(discounted + tax, 2)
    return {"subtotal": round(discounted,2), "tax": tax, "total": total}
