# ifos_form_engine_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, Tuple, List

def validate(form: Dict[str, Any], values: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors=[]
    for f in form.get("fields", []):
        if f.get("required") and f["id"] not in values:
            errors.append(f"Missing: {f['id']}")
    return (len(errors)==0, errors)
