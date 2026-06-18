# ifos_timeline_builder_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def build_timeline(items: List[Dict]) -> List[Dict]:
    # stub: one event per item
    out=[]
    for it in items:
        out.append({"event_id":"evt.gen","kind":"mention","start":it.get("published_at"),"citations":[{"url":it.get("canonical_url")}] })
    return out
