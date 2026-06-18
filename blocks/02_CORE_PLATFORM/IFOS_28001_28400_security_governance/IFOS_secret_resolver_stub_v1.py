# IFOS Secret Resolver Stub v1
from __future__ import annotations
from typing import Dict, Any

class SecretStore:
    def __init__(self):
        self._values: Dict[str, str] = {}
    def put(self, secret_ref: str, value: str) -> None:
        self._values[secret_ref] = value
    def resolve(self, secret_ref: str) -> str:
        if secret_ref not in self._values:
            raise KeyError(f"Secret not found: {secret_ref}")
        return self._values[secret_ref]

def resolve_headers(config: Dict[str, Any], store: SecretStore) -> Dict[str, str]:
    # Example config: {"headers": {"Authorization": "secretref.xyz"}}
    out = {}
    for k, v in (config.get("headers") or {}).items():
        if isinstance(v, str) and v.startswith("secretref."):
            out[k] = store.resolve(v)
        else:
            out[k] = v
    return out
