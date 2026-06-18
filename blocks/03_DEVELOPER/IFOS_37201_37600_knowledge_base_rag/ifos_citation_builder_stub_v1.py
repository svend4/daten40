# ifos_citation_builder_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List

def build_citations(selected: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    cites=[]
    for it in selected:
        cites.append({
            "doc_id": it.get("doc_id"),
            "chunk_id": it.get("chunk_id"),
            "offsets": it.get("offsets", {"start":0,"end":0}),
            "locator": it.get("locator", {})
        })
    return cites
