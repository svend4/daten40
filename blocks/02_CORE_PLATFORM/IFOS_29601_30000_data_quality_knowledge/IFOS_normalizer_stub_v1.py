# IFOS Normalizer Stub v1
from __future__ import annotations
from typing import Dict, Any

def normalize(raw: Dict[str, Any]) -> Dict[str, Any]:
    payload = raw.get("payload", {})
    # naive normalization (real system will parse HTML/RSS/JSON)
    url = payload.get("url","")
    title = payload.get("title") or "Untitled"
    summary = payload.get("summary") or ""
    return {
        "canonical_url": url,
        "title": title,
        "summary": summary,
        "language": "ru",
        "region": "EU",
        "tags": [],
        "entities": [],
    }
