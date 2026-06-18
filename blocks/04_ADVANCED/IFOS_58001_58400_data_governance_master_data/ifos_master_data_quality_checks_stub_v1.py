# ifos_master_data_quality_checks_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def check(entity: Dict) -> List[str]:
    errors=[]
    if not entity.get("names",{}).get("canonical"):
        errors.append("missing_canonical_name")
    dom = (entity.get("identifiers") or {}).get("domain")
    if entity.get("type")=="organization" and not dom:
        errors.append("missing_domain")
    return errors
