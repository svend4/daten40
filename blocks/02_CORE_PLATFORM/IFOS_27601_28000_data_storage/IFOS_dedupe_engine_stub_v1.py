# IFOS Dedupe Engine Stub v1
from __future__ import annotations
from typing import Dict, Any, List, Tuple
import hashlib

def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def compute_hashes(item: Dict[str, Any]) -> Dict[str, str]:
    url = item.get("url","")
    content = item.get("content","")
    title = item.get("title","")
    return {
        "url_hash": "sha256:" + sha256(url),
        "content_hash": "sha256:" + sha256(content),
        "title_hash": "sha256:" + sha256(title),
    }

def exact_dedupe(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out = []
    for it in items:
        h = it.get("hashes", {}).get("content_hash") or compute_hashes(it)["content_hash"]
        if h in seen:
            continue
        seen.add(h)
        out.append(it)
    return out
