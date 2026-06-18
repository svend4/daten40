# IFOS Entity Resolver Stub v1
from __future__ import annotations
from typing import Dict, Any, List, Tuple
import re

def extract_entities(record: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Stub: naive extraction. Replace with NER/LLM extraction + evidence spans."""
    text = record.get("text","")
    entities: List[Dict[str, Any]] = []
    links: List[Dict[str, Any]] = []
    for m in re.finditer(r"\b([A-Z][A-Za-z]+Corp)\b", text):
        entities.append({
            "entity_id":"ent."+m.group(1).lower(),
            "type":"Org",
            "name":m.group(1),
            "aliases":[],
            "evidence_refs":[record["record_id"]],
            "created_at":"",
            "updated_at":"",
            "version":"1.0.0"
        })
    return entities, links
