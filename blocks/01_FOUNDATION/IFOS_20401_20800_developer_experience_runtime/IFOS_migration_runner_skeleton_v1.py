# IFOS Migration Runner Skeleton v1
from __future__ import annotations
from typing import Dict, Any

def apply_migration(config: Dict[str, Any], migration: Dict[str, Any]) -> Dict[str, Any]:
    # Stub: apply rename/default/transform changes
    # Example: set defaults
    for ch in migration.get("changes", []):
        if ch.get("type") == "default":
            # naive default set if missing
            path = ch.get("path","")
            # real implementation should traverse dict by dotted path
            config.setdefault(path, "DEFAULT")
    return config
