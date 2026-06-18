# IFOS Usage Billing Aggregator Skeleton v1
# Aggregates usage events into an invoice for a tenant + plan.

from __future__ import annotations
from typing import List, Dict, Any
from dataclasses import dataclass
import datetime

def sum_meter(events: List[Dict[str, Any]], key: str) -> float:
    return float(sum((e.get("meters") or {}).get(key, 0) for e in events))

def apply_allowance(qty: float, allowance: float) -> float:
    return max(0.0, qty - allowance)

def make_invoice(tenant_id: str, plan: Dict[str, Any], events: List[Dict[str, Any]], period_from: str, period_to: str) -> Dict[str, Any]:
    rates = plan["rates"]
    allowance = plan.get("free_allowance") or {}

    qty_runs = apply_allowance(sum_meter(events,"runs"), allowance.get("runs",0))
    qty_steps = sum_meter(events,"steps")
    qty_requests = apply_allowance(sum_meter(events,"requests"), allowance.get("requests",0))
    qty_storage = apply_allowance(sum_meter(events,"storage_mb_day"), allowance.get("storage_mb_day",0))
    qty_verified = sum_meter(events,"verified_evidence")

    lines = [
        {"meter":"runs","qty":qty_runs,"unit_price":rates["per_run"],"amount":qty_runs*rates["per_run"]},
        {"meter":"steps","qty":qty_steps,"unit_price":rates["per_step"],"amount":qty_steps*rates["per_step"]},
        {"meter":"requests","qty":qty_requests,"unit_price":rates["per_request"],"amount":qty_requests*rates["per_request"]},
        {"meter":"storage_mb_day","qty":qty_storage,"unit_price":rates["per_storage_mb_day"],"amount":qty_storage*rates["per_storage_mb_day"]},
        {"meter":"verified_evidence","qty":qty_verified,"unit_price":rates["per_verified_evidence"],"amount":qty_verified*rates["per_verified_evidence"]},
    ]
    subtotal = sum(l["amount"] for l in lines)
    invoice = {
        "invoice_id": f"inv.{tenant_id}.{period_from[:7]}",
        "tenant_id": tenant_id,
        "plan_id": plan["plan_id"],
        "period":{"from":period_from,"to":period_to},
        "currency": plan["currency"],
        "lines": lines,
        "subtotal": round(subtotal, 6),
        "tax": 0.0,
        "total": round(subtotal, 6),
        "status":"draft",
        "created_at": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z",
    }
    return invoice

if __name__ == "__main__":
    plan = {"plan_id":"plan.pro","currency":"EUR","rates":{"per_run":0.01,"per_step":0.001,"per_request":0.002,"per_storage_mb_day":0.0002,"per_verified_evidence":0.5},
            "free_allowance":{"runs":1000,"requests":2000,"storage_mb_day":500}}
    events = [{"meters":{"runs":2,"steps":42,"requests":45,"storage_mb_day":1.5,"verified_evidence":1}}]
    print(make_invoice("ten.demo", plan, events, "2026-01-01","2026-01-31"))
