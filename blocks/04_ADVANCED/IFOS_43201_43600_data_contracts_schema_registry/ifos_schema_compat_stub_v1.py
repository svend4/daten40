# ifos_schema_compat_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List

def compare(old: Dict[str, Any], new: Dict[str, Any]) -> List[Dict[str, Any]]:
    # stub: detect removed required fields and added required fields
    diff: List[Dict[str, Any]]=[]
    old_req=set(old.get("required", []))
    new_req=set(new.get("required", []))
    removed=old_req - new_req
    added=new_req - old_req
    for r in sorted(removed):
        diff.append({"change":"removed_required","field":r,"severity":"breaking"})
    for a in sorted(added):
        diff.append({"change":"added_required","field":a,"severity":"breaking"})
    # added optional fields are minor
    old_props=set((old.get("properties") or {}).keys())
    new_props=set((new.get("properties") or {}).keys())
    for p in sorted(new_props-old_props):
        diff.append({"change":"added_optional_field","field":p,"severity":"minor"})
    return diff
