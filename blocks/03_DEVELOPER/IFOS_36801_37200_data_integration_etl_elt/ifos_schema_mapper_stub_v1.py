# ifos_schema_mapper_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def apply_mapping(record: Dict[str, Any], rules: list[Dict[str, Any]]) -> Dict[str, Any]:
    out=dict(record)
    for r in rules:
        op=r.get("op")
        if op=="rename":
            frm=r["from"]; to=r["to"]
            if frm in out:
                out[to]=out.pop(frm)
        elif op=="cast":
            field=r["field"]; to=r["to"]
            if field in out and to=="number":
                try: out[field]=float(out[field])
                except Exception: pass
        elif op=="normalize_email":
            field=r["field"]
            if field in out and isinstance(out[field], str):
                out[field]=out[field].strip().lower()
    return out
