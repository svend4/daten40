# ifos_intent_to_capabilities_stub_v1.py
from __future__ import annotations
from typing import Dict

MAP={
 "term.data.fetch.rss":["data.fetch.rss"],
 "term.notify.telegram.send":["notify.telegram.send"],
 "term.data.dedup":["data.dedup"],
 "term.ai.summarize":["ai.text.summarize"],
}

def map_terms(terms):
    caps=[]
    for t in terms:
        caps+=MAP.get(t,[])
    return sorted(set(caps))
