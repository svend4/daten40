# IFOS Feedback Aggregator Stub v1
from __future__ import annotations
from typing import Dict, Any, List, DefaultDict
from collections import defaultdict

def aggregate(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    # compute simple success rate per canonical_id
    counts=defaultdict(lambda: {"run_success":0,"run_fail":0,"click":0,"install":0})
    for e in events:
        cid=e["canonical_id"]
        t=e["event_type"]
        if t in counts[cid]:
            counts[cid][t]+=1
    signals={}
    for cid,c in counts.items():
        total=c["run_success"]+c["run_fail"]
        sr=(c["run_success"]/total) if total>0 else None
        signals[cid]={"success_rate": sr, "popularity": c["click"]+2*c["install"]}
    return signals
