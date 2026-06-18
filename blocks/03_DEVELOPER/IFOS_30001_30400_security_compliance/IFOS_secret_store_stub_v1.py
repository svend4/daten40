# IFOS Secret Store Stub v1
from __future__ import annotations
from typing import Dict, Any

class SecretStore:
    def __init__(self):
        self._refs = {}
        self._values = {}

    def create_ref(self, name: str, purpose: str) -> str:
        sid = "sec_" + str(len(self._refs)+1)
        self._refs[sid] = {"name": name, "purpose": purpose}
        return sid

    def set_value(self, name: str, value: str) -> None:
        self._values[name] = value

    def has(self, name: str) -> bool:
        return name in self._values
