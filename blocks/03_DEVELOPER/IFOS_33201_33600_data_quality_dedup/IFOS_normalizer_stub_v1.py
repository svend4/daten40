# IFOS Normalizer Stub v1
from __future__ import annotations
from typing import Dict, Any, List
import re

def clean_title(title: str) -> str:
    title=title.strip()
    title=re.sub(r"\s+", " ", title)
    return title

def normalize_raw(raw: Dict[str, Any], rules: List[Dict[str, Any]]) -> Dict[str, Any]:
    payload=raw.get("payload", {})
    title=payload.get("name") or payload.get("title") or "Untitled"
    title=clean_title(title)
    # apply simple regex cleanup rules
    for r in rules:
        if not r.get("enabled", True):
            continue
        if r.get("kind")=="title_cleanup" and r.get("pattern"):
            title=re.sub(r["pattern"], r.get("action",{}).get("replace_with",""), title).strip()
    return {
        "canonical_id": "canon_stub",
        "title": title,
        "kind": payload.get("kind","unknown"),
        "capabilities": payload.get("capabilities", [])
    }
