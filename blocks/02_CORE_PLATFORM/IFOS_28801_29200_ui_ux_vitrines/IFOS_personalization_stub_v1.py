# IFOS Personalization Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def pick_home_vitrines(prefs: Dict[str, Any], available: List[str]) -> List[str]:
    # Simple rule: pinned first, then favorites, fallback to first N.
    pinned = prefs.get("pinned",[]) or []
    fav = prefs.get("favorites",[]) or []
    out = []
    for x in pinned + fav:
        if x in available and x not in out:
            out.append(x)
    for x in available:
        if len(out) >= 6:
            break
        if x not in out:
            out.append(x)
    return out
