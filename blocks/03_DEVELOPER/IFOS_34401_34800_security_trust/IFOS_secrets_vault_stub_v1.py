# IFOS Secrets Vault Stub v1
from __future__ import annotations
from typing import Dict, Any

VAULT: Dict[str, Dict[str, Any]] = {}

def put(secret_id: str, value: str, meta: Dict[str, Any]) -> None:
    VAULT[secret_id]={"value":value,"meta":meta}

def get(secret_id: str, scope: str) -> str:
    # scope checks omitted in stub
    if secret_id not in VAULT:
        raise KeyError("secret not found")
    return VAULT[secret_id]["value"]
