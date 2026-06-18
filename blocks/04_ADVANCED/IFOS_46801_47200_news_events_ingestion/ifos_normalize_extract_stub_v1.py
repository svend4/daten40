# ifos_normalize_extract_stub_v1.py
from __future__ import annotations
from typing import Dict

def normalize(raw: Dict) -> Dict:
    # stub: minimal normalization
    return {"canonical_url": raw.get("url"), "title": raw.get("title",""), "body_text":"clean", "language":"en"}
