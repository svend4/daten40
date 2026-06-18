# ifos_data_quality_checks_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def validate_email(val: str) -> bool:
    return isinstance(val, str) and ("@" in val) and ("." in val)

def run_check(record: Dict[str, Any], check: Dict[str, Any]) -> bool:
    if check.get("type")=="validity":
        field=check["rule"].get("field")
        if field:
            return validate_email(record.get(field, ""))
    return True
