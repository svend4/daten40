# ifos_retriever_stub_v1.py
from __future__ import annotations
from typing import List, Dict, Any

def retrieve(query_vec: List[float], items: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
    # items: {"chunk_id":..., "vec":[...]}
    def dot(a,b): return sum(x*y for x,y in zip(a,b))
    scored=[{"chunk_id":it["chunk_id"], "score":dot(query_vec,it["vec"]), "doc_id":it.get("doc_id")} for it in items]
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
