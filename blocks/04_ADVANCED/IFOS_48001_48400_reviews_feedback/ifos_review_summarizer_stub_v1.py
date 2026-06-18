# ifos_review_summarizer_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def summarize(reviews: List[Dict]) -> Dict:
    return {"topics":[{"topic":"bugs","count":len(reviews)}],"trends":{},"fit":{}}
