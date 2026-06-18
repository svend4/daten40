# ifos_ledger_posting_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def post(ledger: Dict[str, Any], entry: Dict[str, Any]) -> Dict[str, Any]:
    ledger.setdefault("entries", []).append(entry)
    ledger["balance"]=float(ledger.get("balance",0.0)) + float(entry.get("amount",0.0))
    # simplistic reserve logic
    reserve=float(ledger.get("reserves",0.0) or 0.0)
    ledger["available"]=max(0.0, ledger["balance"]-reserve)
    return ledger
