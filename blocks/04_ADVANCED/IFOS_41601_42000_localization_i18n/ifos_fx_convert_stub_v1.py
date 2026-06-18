# ifos_fx_convert_stub_v1.py
from __future__ import annotations
from typing import Dict

def convert(amount: float, from_ccy: str, to_ccy: str, rates: Dict[str, float], base: str) -> float:
    # rates are base -> ccy
    if from_ccy==to_ccy: return amount
    if from_ccy!=base:
        amount = amount / float(rates[from_ccy])
    return amount * float(rates[to_ccy])
