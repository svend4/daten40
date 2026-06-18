# ifos_kw_tagger_stub_v1.py
from __future__ import annotations
from typing import List

def suggest_tags(text: str) -> List[str]:
    tags=[]
    for t in ["news","portal","reviews","marketplace","ops","security"]:
        if t in text.lower():
            tags.append(t)
    return tags
