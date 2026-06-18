# ifos_invoice_builder_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List

def build(tenant_id: str, period: Dict[str, Any], lines: List[Dict[str, Any]], currency: str = "EUR") -> Dict[str, Any]:
    total=sum(float(l.get("amount",0.0)) for l in lines)
    return {"tenant_id": tenant_id, "period": period, "lines": lines, "total": total, "currency": currency, "status":"draft"}
