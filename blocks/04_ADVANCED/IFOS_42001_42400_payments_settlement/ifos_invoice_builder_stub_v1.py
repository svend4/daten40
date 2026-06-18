# ifos_invoice_builder_stub_v1.py
from __future__ import annotations
from typing import List, Dict, Any

def totals(items: List[Dict[str, Any]], tax_rate: float) -> Dict[str, float]:
    subtotal=sum(float(i["qty"])*float(i["unit_price"]) for i in items)
    tax=subtotal*tax_rate
    return {"subtotal": subtotal, "tax": tax, "total": subtotal+tax}
