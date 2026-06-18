# ifos_payouts_split_stub_v1.py
from __future__ import annotations
from typing import List, Dict

def split(gross: float, splits: List[Dict]) -> Dict:
    out={}
    for s in splits:
        out[s["party"]] = gross * (s["percent"]/100.0)
    return out
