# IFOS Entity Resolver Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def extract_entities_simple(text: str) -> List[str]:
    # Placeholder: replace with NER model or dictionary match
    ents=[]
    for token in ["Apple","Google","Microsoft","Telegram","WordPress","Make","n8n"]:
        if token.lower() in text.lower():
            ents.append(token)
    return sorted(set(ents))

def resolve_entities(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    entity_map={}
    for r in records:
        for e in r.get("entities", []):
            entity_map.setdefault(e, {"type":"org","names":[e]})
    return {"entities": entity_map}
