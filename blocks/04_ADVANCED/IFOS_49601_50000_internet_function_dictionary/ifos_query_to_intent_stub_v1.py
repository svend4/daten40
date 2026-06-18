# ifos_query_to_intent_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def parse(query: str) -> Dict:
    q=query.lower()
    intent="build"
    if "сравн" in q: intent="compare"
    terms=[]
    if "rss" in q: terms.append("term.data.fetch.rss")
    if "telegram" in q or "телеграм" in q: terms.append("term.notify.telegram.send")
    if "дубл" in q: terms.append("term.data.dedup")
    return {"intent_type":intent,"terms":terms,"constraints":[]}
