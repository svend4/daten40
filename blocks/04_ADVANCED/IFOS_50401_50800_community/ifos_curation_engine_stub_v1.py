# ifos_curation_engine_stub_v1.py
from __future__ import annotations
from typing import List, Dict

def pick_top(items: List[Dict], n:int=10) -> List[Dict]:
    return sorted(items, key=lambda x: x.get("score",0), reverse=True)[:n]
