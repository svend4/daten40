# IFOS Invoice Generator Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def generate_invoice(order: Dict[str, Any], lines: List[Dict[str, Any]], buyer: Dict[str, Any], seller: Dict[str, Any]) -> Dict[str, Any]:
    subtotal=sum(float(l["amount"]) for l in lines if l.get("tax_rate") is not None or l.get("tax_rate") is None)
    total=float(order["amount_total"])
    return {
        "invoice_id":"inv_stub",
        "order_id":order["order_id"],
        "buyer":buyer,
        "seller":seller,
        "lines":lines,
        "amount_total":total,
        "currency":order["currency"],
        "status":"issued"
    }
