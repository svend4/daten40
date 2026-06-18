# ifos_i18n_loader_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def t(pack: Dict[str, Any], key: str, default: str = "") -> str:
    return pack.get("strings", {}).get(key, default or key)
