# IFOS Search Indexer Stub v1
from __future__ import annotations
from typing import Dict, Any, List
import re

def index_entities(entities: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Minimal in-memory index: keyword -> refs
    idx = {}
    for e in entities:
        text = " ".join([str(e.get(k,"")) for k in ("title","term","question","answer") if k in e])
        words = set(re.findall(r"[A-Za-zА-Яа-я0-9_]+", text.lower()))
        ref = e.get("page_id") or e.get("term_id") or e.get("faq_id") or e.get("tutorial_id") or e.get("case_id") or e.get("doc_card_id") or e.get("explain_id")
        for w in words:
            idx.setdefault(w, set()).add(ref)
    return {"index": {k: sorted(list(v)) for k,v in idx.items()}}

def search(index: Dict[str, Any], query: str) -> List[str]:
    words = re.findall(r"[A-Za-zА-Яа-я0-9_]+", query.lower())
    hits = None
    for w in words:
        s = set(index["index"].get(w, []))
        hits = s if hits is None else hits.intersection(s)
    return sorted(list(hits or []))
