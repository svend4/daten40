# IFOS Adapter Registry Stub v1
from __future__ import annotations
from typing import Dict, Any

_ADAPTERS: Dict[str, Dict[str, Any]] = {}

def register_adapter(adapter: Dict[str, Any]) -> str:
    _ADAPTERS[adapter["adapter_id"]] = adapter
    return adapter["adapter_id"]

def find_adapter(contract_id: str, target_platform: str) -> Dict[str, Any] | None:
    for a in _ADAPTERS.values():
        if a.get("from_contract_id")==contract_id and a.get("to_platform")==target_platform:
            return a
    return None
