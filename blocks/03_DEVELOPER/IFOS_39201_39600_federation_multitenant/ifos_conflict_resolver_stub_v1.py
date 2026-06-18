# ifos_conflict_resolver_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def resolve(conflict: Dict[str, Any]) -> Dict[str, Any]:
    strategy=conflict.get("strategy")
    if strategy == "semver_prefer_high":
        # stub: choose left as higher
        return {"status":"resolved","chosen":"left"}
    if strategy == "last_write_wins":
        return {"status":"resolved","chosen":"right"}
    return {"status":"needs_manual_merge"}
