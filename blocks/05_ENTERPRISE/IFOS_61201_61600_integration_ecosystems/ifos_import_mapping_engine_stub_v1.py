# ifos_import_mapping_engine_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def apply_rules(asset: Dict, rules: List[Dict]) -> Dict:
    tags=set(asset.get("capabilities", []))
    out={"category":"unknown","entity_type":"asset","tags":list(tags)}
    for r in rules:
        match=r.get("match",{})
        cap=match.get("capability_contains")
        if cap and cap in tags:
            out.update(r.get("map_to", {}))
    return out
