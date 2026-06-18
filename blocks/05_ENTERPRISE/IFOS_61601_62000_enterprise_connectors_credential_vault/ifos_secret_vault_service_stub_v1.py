# ifos_secret_vault_service_stub_v1.py
from __future__ import annotations
from typing import Dict
import time

class Vault:
    def __init__(self):
        self._store: Dict[str, Dict] = {}

    def create(self, meta: Dict) -> str:
        sid = meta["secret_id"]
        self._store[sid] = meta
        return sid

    def issue_ephemeral(self, secret_id: str, ttl_seconds: int = 60) -> Dict:
        # returns token without secret value
        return {"token": f"tok-{secret_id}-{int(time.time())}", "expires_in": ttl_seconds}
