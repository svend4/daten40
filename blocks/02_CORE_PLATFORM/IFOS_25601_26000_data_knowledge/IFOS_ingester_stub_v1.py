# IFOS Ingester Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def ingest(source: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Returns list of DataItem-like dicts (raw).
    Replace with RSS/HTML/PDF/API adapters; use Runtime OS for secrets and receipts.
    """
    item_id = "item.demo"
    return [{
        "item_id": item_id,
        "kind": source.get("type","html"),
        "status": "raw",
        "source_id": source["source_id"],
        "payload_ref": f"blob://payloads/{item_id}.raw",
        "meta": {"title":"demo", "lang":"en", "canonical_url": "https://example.com/demo"},
        "policy_ref": "sp.default",
        "provenance_ref": "prov.demo",
        "created_at": "",
        "updated_at": "",
        "version": "1.0.0"
    }]
