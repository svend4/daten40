# IFOS Compatibility Checker Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def check(compat: Dict[str, Any], env: Dict[str, Any]) -> Dict[str, Any]:
    # env: {"ifos_version":"1.0.0","modules":[...],"connectors":[...],"capabilities":[...]}
    missing = {"modules":[], "connectors":[], "capabilities":[]}
    for k in ["modules","connectors","capabilities"]:
        need = set(compat.get(k,[]) or [])
        have = set(env.get(k,[]) or [])
        for x in sorted(need - have):
            missing[k].append(x)
    ok = (not missing["modules"] and not missing["connectors"] and not missing["capabilities"])
    return {"ok": ok, "missing": missing, "min_ifos_version": compat.get("min_ifos_version")}
