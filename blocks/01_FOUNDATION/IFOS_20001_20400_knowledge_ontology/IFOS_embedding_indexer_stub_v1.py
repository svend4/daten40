# IFOS Embedding Indexer Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def build_text(entity: Dict[str, Any]) -> str:
    parts=[entity.get("display", {}).get("title",""), entity.get("display", {}).get("summary","")]
    parts += entity.get("tags", [])
    parts += entity.get("capabilities", [])
    return " | ".join([p for p in parts if p])

def index_entities(entities: List[Dict[str, Any]], model_name: str = "text-embedding-3-large") -> Dict[str, Any]:
    # Stub: call embedding model elsewhere; store vector refs
    items=[]
    for e in entities:
        items.append({"entity_id": e["entity_id"], "vector_ref": f"vec://{e['entity_id']}", "text_ref": build_text(e)})
    return {"index_id": "index.generated", "model": model_name, "dims": 0, "items": items}
