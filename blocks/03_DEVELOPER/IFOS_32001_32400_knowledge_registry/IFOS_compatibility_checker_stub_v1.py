# IFOS Compatibility Checker Stub v1
from __future__ import annotations
from typing import Dict, Any

def is_compatible(matrix: Dict[str, Any], context: Dict[str, Any]) -> bool:
    # minimal check: OS and platform name match if provided
    os_ok = True
    if context.get("os") and matrix.get("oses"):
        os_ok = context["os"].lower() in [o.lower() for o in matrix["oses"]]
    plat_ok = True
    if context.get("platform") and matrix.get("platforms"):
        plat_ok = any(context["platform"].lower() == p.get("name","").lower() for p in matrix["platforms"])
    return os_ok and plat_ok
