# IFOS Search Engine Stub v1 (in-memory)
from __future__ import annotations
from typing import Dict, Any, List, Tuple
import re

def tokenize(s: str) -> List[str]:
    return [t for t in re.split(r"\W+", (s or "").lower()) if t]

def match_score(query: str, doc_text: str) -> float:
    q=set(tokenize(query))
    d=set(tokenize(doc_text))
    if not q:
        return 0.0
    return len(q & d) / len(q)

def apply_filters(doc: Dict[str, Any], filters: Dict[str, Any]) -> bool:
    facets=doc.get("facets", {})
    for k,v in (filters or {}).items():
        if v is None:
            continue
        doc_v=facets.get(k)
        if isinstance(v, list):
            if isinstance(doc_v, list):
                if not set(v).intersection(set(doc_v)):
                    return False
            else:
                if doc_v not in v:
                    return False
        else:
            if doc_v != v:
                return False
    return True

def search(docs: List[Dict[str, Any]], q: Dict[str, Any]) -> List[Tuple[Dict[str, Any], float]]:
    query=q.get("text","") or ""
    filters=q.get("filters", {}) or {}
    out=[]
    for d in docs:
        if not apply_filters(d, filters):
            continue
        s=match_score(query, d.get("text",""))
        out.append((d, s))
    out.sort(key=lambda x: x[1], reverse=True)
    return out
