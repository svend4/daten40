# IFOS RBAC Engine Stub v1
from __future__ import annotations
from typing import Dict, Any, Set

def has_permission(user: Dict[str, Any], perm: str, scope: Dict[str, str]) -> bool:
    # user: {"roles":[{"permissions":[...]}], "scopes":[...]} simplified
    perms:set[str]=set()
    for r in user.get("roles", []):
        for p in r.get("permissions", []):
            perms.add(p)
    return perm in perms
