# IFOS Normalizer Stub v1
from __future__ import annotations
from typing import Dict, Any
import hashlib

def normalize(data_item: Dict[str, Any], raw_text: str) -> Dict[str, Any]:
    text = raw_text.strip()
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return {
        "record_id": "rec.demo",
        "item_id": data_item["item_id"],
        "text": text,
        "summary": text[:160],
        "lang": data_item.get("meta",{}).get("lang","und"),
        "content_hash": "sha256:"+h,
        "canonical_url": data_item.get("meta",{}).get("canonical_url",""),
        "published_at": data_item.get("meta",{}).get("published_at",""),
        "structure": {},
        "created_at": "",
        "updated_at": "",
        "version": "1.0.0"
    }
