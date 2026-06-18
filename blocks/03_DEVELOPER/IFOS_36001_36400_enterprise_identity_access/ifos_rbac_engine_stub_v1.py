# ifos_rbac_engine_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def allowed(user_roles: List[str], role_permissions: Dict[str, List[str]], perm: str) -> bool:
    for r in user_roles:
        if perm in role_permissions.get(r, []):
            return True
    return False
