# IFOS Contract Validator Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def validate_contract(contract: Dict[str, Any], type_names: List[str]) -> Dict[str, Any]:
    findings=[]
    status="pass"
    for inp in contract.get("inputs", []):
        if inp.get("type") not in type_names:
            status="fail"; findings.append(f"unknown type: {inp.get('type')} for input {inp.get('name')}")
    for out in contract.get("outputs", []):
        if out.get("type") not in type_names:
            status="fail"; findings.append(f"unknown type: {out.get('type')} for output {out.get('name')}")
    if any("pii" in (i.get("semantics") or []) for i in contract.get("inputs", [])):
        if "no_log_fields" not in (contract.get("policy") or {}):
            status="warn"; findings.append("PII semantics present but no_log_fields not declared")
    if not contract.get("errors"):
        status="warn"; findings.append("no error handling declared")
    return {"status":status,"findings":findings}
