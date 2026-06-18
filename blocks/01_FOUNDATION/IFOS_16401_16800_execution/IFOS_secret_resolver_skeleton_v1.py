# IFOS Secret Resolver Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List

class SecretVault:
    def __init__(self):
        self._store: Dict[str, Dict[str, str]] = {}

    def put(self, tenant_id: str, name: str, value: str):
        self._store.setdefault(tenant_id, {})[name] = value

    def get(self, tenant_id: str, name: str) -> str:
        return self._store.get(tenant_id, {}).get(name, "")

class SecretResolver:
    def __init__(self, vault: SecretVault):
        self.vault = vault

    def resolve(self, tenant_id: str, secret_refs: List[Dict[str, Any]]) -> Dict[str, str]:
        resolved: Dict[str, str] = {}
        for s in secret_refs or []:
            # ref format: secret://ten/<tenant>/vault/<name>
            ref = s.get("ref","")
            name = s.get("name","")
            # MVP: use "name" as vault key
            resolved[name] = self.vault.get(tenant_id, name)
        return resolved
