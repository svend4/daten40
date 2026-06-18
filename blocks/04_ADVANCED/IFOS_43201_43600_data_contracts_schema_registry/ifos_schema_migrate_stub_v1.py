# ifos_schema_migrate_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List

def apply_mapping(payload: Dict[str, Any], mappings: List[Dict[str, Any]]) -> Dict[str, Any]:
    # stub: supports only simple copy from one dotted path to another
    def get_path(obj, path):
        cur=obj
        for part in path.split("."):
            if part not in cur: return None
            cur=cur[part]
        return cur
    def set_path(obj, path, val):
        cur=obj
        parts=path.split(".")
        for part in parts[:-1]:
            cur=cur.setdefault(part, {})
        cur[parts[-1]]=val
    out=dict(payload)
    for m in mappings:
        src=m.get("from","").strip("/").replace("/",".")
        dst=m.get("to","").strip("/").replace("/",".")
        val=get_path(out, src)
        if val is not None:
            set_path(out, dst, val)
    return out
