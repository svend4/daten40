# ifos_normalize_mapper_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def normalize(raw: Dict[str, Any]) -> Dict[str, Any]:
    p=raw.get("payload", {})
    title=p.get("title","")
    body=p.get("content","") or p.get("body","")
    links=p.get("links", []) if isinstance(p.get("links", []), list) else []
    return {"title": title, "body": body, "links": links, "locale": "und"}
