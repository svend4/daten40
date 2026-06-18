# IFOS Import Pipeline Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def run_pipeline(source: Dict[str, Any], raws: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Fake stages for demo
    return {
        "source_id": source["source_id"],
        "raw_fetched": len(raws),
        "canonical_created": max(1, len(raws)//10),
        "dedup_candidates": max(0, len(raws)//12),
        "auto_merged": max(0, len(raws)//40),
        "needs_review": max(0, len(raws)//30),
        "quarantined": 0
    }
