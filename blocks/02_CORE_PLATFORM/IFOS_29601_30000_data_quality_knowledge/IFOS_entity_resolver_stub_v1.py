# IFOS Entity Resolver Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def resolve_entities(record: Dict[str, Any], entity_index: Dict[str, str]) -> List[str]:
    # entity_index maps alias->entity_id
    text = (record.get("title","") + " " + record.get("summary","")).lower()
    found = []
    for alias, eid in entity_index.items():
        if alias.lower() in text:
            if eid not in found:
                found.append(eid)
    return found
