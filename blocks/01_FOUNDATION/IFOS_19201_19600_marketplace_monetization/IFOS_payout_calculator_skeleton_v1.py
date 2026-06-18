# IFOS Payout Calculator Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List

def calculate_payout(ledger_entries: List[Dict[str, Any]], revshare: Dict[str, Any]) -> Dict[str, Any]:
    gross = sum(e["amount"] for e in ledger_entries if e["reason"] == "sale")
    platform_fee = sum(e["amount"] for e in ledger_entries if e["reason"] == "platform_fee")
    reserve = sum(e["amount"] for e in ledger_entries if e["reason"] == "chargeback_reserve")
    net = gross - platform_fee - reserve
    return {"gross": gross, "fees": platform_fee, "reserves": reserve, "net": net}
