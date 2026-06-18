# ifos_registry_dependency_resolver_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def resolve(items: List[Dict]) -> Dict:
    # stub: just returns items in given order
    return {"plan":[i.get("item_id") for i in items], "notes":["stub"]}
