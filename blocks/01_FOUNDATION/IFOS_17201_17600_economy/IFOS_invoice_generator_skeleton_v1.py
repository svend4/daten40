# IFOS Invoice Generator Skeleton v1
from __future__ import annotations
from typing import Dict, Any

def generate_invoice(tenant_id: str, usage: Dict[str, Any], pricing: Dict[str, Any]) -> Dict[str, Any]:
    terms = pricing.get("terms", {}) or {}
    included = (terms.get("included_quota", {}) or {}).get("runs", 0)
    runs = int((usage.get("metrics", {}) or {}).get("runs", 0))
    extra_runs = max(0, runs - included)
    per_run = float(terms.get("per_run", 0.0))
    per_1000_steps = float(terms.get("per_1000_steps", 0.0))
    steps = int((usage.get("metrics", {}) or {}).get("steps", 0))
    steps_units = steps/1000.0

    line_items = []
    line_items.append({"name":f"Included quota (runs {included})","qty":1,"unit_price":0.0,"amount":0.0,"subject":usage.get("subject",{}),"usage_ref":usage.get("usage_id","")})
    line_items.append({"name":"Extra runs","qty":extra_runs,"unit_price":per_run,"amount":round(extra_runs*per_run,2),"subject":usage.get("subject",{}),"usage_ref":usage.get("usage_id","")})
    line_items.append({"name":"Steps (per 1000)","qty":steps_units,"unit_price":per_1000_steps,"amount":round(steps_units*per_1000_steps,2),"subject":usage.get("subject",{}),"usage_ref":usage.get("usage_id","")})
    subtotal = round(sum(li["amount"] for li in line_items),2)
    return {
        "invoice_id":"inv.generated",
        "tenant_id":tenant_id,
        "currency":pricing.get("currency","EUR"),
        "period_start":usage.get("period_start",""),
        "period_end":usage.get("period_end",""),
        "line_items":line_items,
        "subtotal":subtotal,
        "tax":0.0,
        "total":subtotal,
        "status":"draft",
        "evidence_refs":[f"usage:{usage.get('usage_id','')}"],
        "created_at":"",
        "version":"1.0.0"
    }
