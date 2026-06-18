# ifos_sync_delta_builder_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def build_delta(from_manifest: Dict, to_manifest: Dict) -> List[str]:
    # Return list of changed files
    a=set(from_manifest.get("files", []))
    b=set(to_manifest.get("files", []))
    return sorted(list((a|b) - (a&b)))
