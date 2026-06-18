# ifos_contract_tester_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List

def validate_io(contract: Dict[str, Any], sample_input: Dict[str, Any], sample_output: Dict[str, Any]) -> List[str]:
    # Placeholder: returns empty list if 'query' exists when required
    errors=[]
    req = contract.get("input_schema",{}).get("required",[])
    for r in req:
        if r not in sample_input:
            errors.append(f"missing_input:{r}")
    return errors
