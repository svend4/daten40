# ifos_plugin_loader_stub_v1.py
from __future__ import annotations
from typing import Dict, Any
import importlib

def load(entry: str) -> Any:
    mod, fn = entry.split(":")
    m=importlib.import_module(mod)
    return getattr(m, fn)
