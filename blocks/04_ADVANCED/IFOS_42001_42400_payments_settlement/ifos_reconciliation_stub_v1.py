# ifos_reconciliation_stub_v1.py
from __future__ import annotations
from typing import List, Dict, Any

def reconcile(invoices: List[Dict[str, Any]], settlements: List[Dict[str, Any]]) -> Dict[str, Any]:
    inv_total=sum(float(i.get("totals",{}).get("total",0.0)) for i in invoices)
    set_total=sum(float(s.get("amount",0.0)) for s in settlements)
    return {"invoice_total": inv_total, "settlement_total": set_total, "delta": set_total-inv_total}
