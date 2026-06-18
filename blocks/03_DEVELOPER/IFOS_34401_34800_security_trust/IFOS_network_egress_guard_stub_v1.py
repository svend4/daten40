# IFOS Network Egress Guard Stub v1
from __future__ import annotations
from typing import Dict, Any, Tuple
import fnmatch

def allowed(dest: str, netpol: Dict[str, Any]) -> Tuple[bool, str]:
    mode=netpol.get("mode","custom")
    allow=netpol.get("allow") or []
    deny=netpol.get("deny") or []
    if mode=="allow_all":
        return True, "allow_all"
    # deny_all_by_default: must match allow, unless explicitly denied
    for pat in deny:
        if fnmatch.fnmatch(dest, pat):
            return False, f"denied by {pat}"
    for pat in allow:
        if fnmatch.fnmatch(dest, pat):
            return True, f"allowed by {pat}"
    if mode=="deny_all_by_default":
        return False, "deny_all_by_default"
    return False, "not allowed"
