# ifos_schema_validator_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def validate(payload: Dict, required: List[str]) -> List[str]:
    errors=[]
    for f in required:
        if f not in payload or payload.get(f) in (None,""):
            errors.append(f"missing:{f}")
    return errors
