# ifos_conflict_resolver_stub_v1.py
from __future__ import annotations
from typing import Dict

def resolve(conflict: Dict, strategy: str="source_priority") -> Dict:
    # returns selected value
    cands=conflict.get("candidates",[])
    if not cands: return {"selected": None}
    if strategy=="last_write_wins":
        return {"selected": sorted(cands, key=lambda x: x.get("ts",""))[-1]}
    # source_priority: first candidate is highest priority in this stub
    return {"selected": cands[0]}
