# IFOS Reconciler Stub v1
from __future__ import annotations
from typing import Dict, Any, List, Callable

def reconcile(records: List[Dict[str, Any]], decide_fn: Callable[[Dict[str, Any], Dict[str, Any]], Dict[str, Any]]) -> Dict[str, Any]:
    merged=0
    conflicts=[]
    kept=[]
    for r in records:
        dup_found=False
        for k in kept:
            d=decide_fn(k, r)
            if d["decision"]=="same":
                merged+=1
                dup_found=True
                break
            if d["decision"]=="unsure":
                conflicts.append({"kind":"dedupe_unsure","items":[k.get("record_id","?"), r.get("record_id","?")], "note":str(d["signals"])})
        if not dup_found:
            kept.append(r)
    return {"records_seen":len(records),"merged":merged,"conflicts":conflicts}
