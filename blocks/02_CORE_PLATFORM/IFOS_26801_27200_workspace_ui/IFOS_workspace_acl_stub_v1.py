# IFOS Workspace ACL Stub v1
from __future__ import annotations
from typing import Dict, Any

ROLE_SCOPES = {
    "viewer": {"cards"},
    "editor": {"cards","flows","packages"},
    "admin": {"cards","flows","packages","secrets","export","admin"},
}

def can(role: str, scope: str) -> bool:
    return scope in ROLE_SCOPES.get(role, set())
