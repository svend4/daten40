# IFOS Truth Policy Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def choose_field(field: str, candidates: List[Dict[str, Any]], source_kind_order: List[str]) -> Dict[str, Any] | None:
    # candidate: {"value":..., "source_kind":..., "freshness":..., "signed":...}
    order={k:i for i,k in enumerate(source_kind_order)}
    best=None
    best_key=(10**9, -1.0)
    for c in candidates:
        pri=order.get(c.get("source_kind"), 10**8)
        fresh=float(c.get("freshness",0.0))
        key=(pri, -fresh)
        if key < best_key:
            best_key=key
            best=c
    return best
