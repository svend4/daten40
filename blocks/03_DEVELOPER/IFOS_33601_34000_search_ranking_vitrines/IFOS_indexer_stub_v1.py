# IFOS Indexer Stub v1
from __future__ import annotations
from typing import Dict, Any, List
import datetime

def build_index_doc(canonical: Dict[str, Any], signals: Dict[str, Any]) -> Dict[str, Any]:
    text_parts=[canonical.get("title",""), canonical.get("description","")]
    text_parts += canonical.get("capabilities", [])
    text=" ".join([p for p in text_parts if p])
    facets={
        "kind": canonical.get("kind"),
        "capability": canonical.get("capabilities", []),
        "risk": canonical.get("risk","unknown"),
        "platform": canonical.get("platform", []),
    }
    return {
        "doc_id": f"doc:{canonical['canonical_id']}",
        "canonical_id": canonical["canonical_id"],
        "kind": canonical.get("kind","unknown"),
        "title": canonical.get("title",""),
        "text": text,
        "facets": facets,
        "signals": signals,
        "updated_at": datetime.datetime.utcnow().isoformat()+"Z",
        "version":"1.0.0"
    }

def reindex(canon_items: List[Dict[str, Any]], signals_by_id: Dict[str, Any]) -> List[Dict[str, Any]]:
    docs=[]
    for c in canon_items:
        docs.append(build_index_doc(c, signals_by_id.get(c["canonical_id"], {})))
    return docs
