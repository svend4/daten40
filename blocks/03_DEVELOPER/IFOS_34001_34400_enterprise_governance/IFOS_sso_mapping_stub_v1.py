# IFOS SSO Mapping Stub v1
from __future__ import annotations
from typing import Dict, Any

def map_groups_to_roles(claims: Dict[str, Any], mapping: Dict[str, str]) -> Dict[str, Any]:
    groups=set(claims.get("groups", []))
    roles=[]
    for g,r in mapping.items():
        if g in groups:
            roles.append(r)
    return {"roles": roles}
