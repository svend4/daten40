# ifos_badge_assigner_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def assign(item_metrics: Dict, badge_defs: List[Dict]) -> List[str]:
    out=[]
    for b in badge_defs:
        ok=True
        for c in b.get("criteria", []):
            k=c["k"]; op=c["op"]; v=c["v"]
            val=item_metrics.get(k)
            if val is None: ok=False; break
            if op==">=" and not (val>=v): ok=False
            if op=="<=" and not (val<=v): ok=False
        if ok: out.append(b["badge_id"])
    return out
