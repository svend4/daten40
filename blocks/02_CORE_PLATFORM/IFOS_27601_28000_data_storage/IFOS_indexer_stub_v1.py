# IFOS Indexer Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def build_fulltext_index(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Placeholder: real implementation would use a search engine.
    tokens = 0
    for r in records:
        tokens += len((r.get("title","") + " " + r.get("content","")).split())
    return {"docs": len(records), "tokens": tokens}
