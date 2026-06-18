# IFOS Secret Store Stub v1
from __future__ import annotations
from typing import Dict, Optional

class SecretStore:
    def __init__(self):
        self._data: Dict[str, str] = {}

    def put(self, secret_ref: str, value: str) -> None:
        self._data[secret_ref] = value

    def get(self, secret_ref: str) -> Optional[str]:
        return self._data.get(secret_ref)

    def rotate(self, secret_ref: str, new_value: str) -> None:
        self._data[secret_ref] = new_value
