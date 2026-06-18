# ifos_schema_validate_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List

def validate(payload: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    # lightweight stub validator (not full JSON Schema)
    errors: List[Dict[str, Any]]=[]
    required=schema.get("required", [])
    for r in required:
        if r not in payload:
            errors.append({"path":f"/{r}","message":"Missing required"})
    # check a minimal 'type' map for top-level properties
    props=schema.get("properties", {})
    for k,v in props.items():
        if k in payload and "type" in v:
            t=v["type"]
            if t=="number" and not isinstance(payload[k], (int,float)):
                errors.append({"path":f"/{k}","expected":"number","got":type(payload[k]).__name__})
            if t=="string" and not isinstance(payload[k], str):
                errors.append({"path":f"/{k}","expected":"string","got":type(payload[k]).__name__})
    return {"ok": len(errors)==0, "errors": errors, "warnings": []}
