# IFOS RAG Retriever Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def rag_query(query: Dict[str, Any], candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Stub: returns first candidate summary as answer with citation."""
    if not candidates:
        return {
            "result_id":"res.demo",
            "query_id":query["query_id"],
            "answer":"No data",
            "citations":[],
            "confidence":0.0,
            "updated_at":"",
            "version":"1.0.0"
        }
    rec=candidates[0]
    return {
        "result_id":"res.demo",
        "query_id":query["query_id"],
        "answer":rec.get("summary",""),
        "citations":[{"record_id":rec["record_id"],"span":"summary","score":0.5}],
        "entities":[],
        "confidence":0.3,
        "warnings":["stub"],
        "updated_at":"",
        "version":"1.0.0"
    }
