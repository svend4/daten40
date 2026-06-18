# ifos_data_steward_queue_stub_v1.py
from __future__ import annotations
from typing import List, Dict

def build_queue(link_candidates: List[Dict]) -> List[Dict]:
    # Prioritize by score desc
    return sorted(link_candidates, key=lambda x: x.get("score",0), reverse=True)
