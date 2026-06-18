# ifos_extractor_router_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def route(content_type: str) -> str:
    if "html" in content_type: return "html_article_extractor"
    if "json" in content_type: return "json_object_extractor"
    if "pdf" in content_type: return "pdf_text_extractor"
    return "generic_extractor"

def extract(extractor_id: str, payload: Any) -> Dict[str, Any]:
    # stub: just wrap payload
    return {"kind":"generic","payload": payload}
