# ifos_ui_shortcut_resolver_stub_v1.py
from __future__ import annotations
from typing import Dict

def resolve(keys: str, mapping: Dict[str, str]) -> str:
    return mapping.get(keys, "noop")
