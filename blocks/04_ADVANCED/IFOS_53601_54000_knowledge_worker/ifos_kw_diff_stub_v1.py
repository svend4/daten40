# ifos_kw_diff_stub_v1.py
from __future__ import annotations
from typing import Dict

def diff(old: Dict, new: Dict) -> Dict:
    out={}
    for k in set(old.keys()) | set(new.keys()):
        if old.get(k) != new.get(k):
            out[k]={"from":old.get(k), "to":new.get(k)}
    return out
