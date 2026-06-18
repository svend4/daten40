# IFOS Compatibility Checker Stub v1
from __future__ import annotations
from typing import Dict, Any

def is_compatible(matrix: Dict[str, Any], runtime: str, runtime_version: str) -> bool:
    for s in matrix.get("supported", []):
        if s.get("runtime") == runtime:
            # stub: accept any version when runtime matches
            return True
    return False
