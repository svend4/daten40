# IFOS Marketplace Indexer Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def build_index(items: List[Dict[str, Any]], packages: List[Dict[str, Any]], vitrines: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "index_id": "idx.demo",
        "items": [i["item_id"] for i in items],
        "packages": [p["package_id"] for p in packages],
        "vitrines": [v["vitrine_id"] for v in vitrines],
        "channels": ["stable", "beta", "nightly"],
        "updated_at": "",
        "version": "1.0.0"
    }
