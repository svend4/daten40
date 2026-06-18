# IFOS Secret Vault Stub v1
from __future__ import annotations
from typing import Dict, Any

_VAULT: Dict[str, Dict[str, Any]] = {}

def register_secret_ref(secret_ref: Dict[str, Any]) -> str:
    _VAULT[secret_ref["secret_id"]] = {"ref": secret_ref, "value": None}
    return secret_ref["secret_id"]

def put_secret_value(secret_id: str, value: str) -> None:
    if secret_id not in _VAULT:
        raise KeyError("unknown secret_id")
    _VAULT[secret_id]["value"] = value

def get_secret_value(secret_id: str) -> str:
    # In real system: enforce ACL + audit log.
    if secret_id not in _VAULT or _VAULT[secret_id]["value"] is None:
        raise KeyError("secret missing")
    return _VAULT[secret_id]["value"]
