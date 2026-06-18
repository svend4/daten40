# IFOS One-click Installer Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def run_install(recipe: Dict[str, Any]) -> Dict[str, Any]:
    steps = recipe.get("steps", []) or []
    executed = []
    for s in steps:
        executed.append({"kind": s.get("kind"), "name": s.get("name"), "status":"ok"})
    sanity = recipe.get("sanity_check", {}) or {}
    result = {"status":"ok","executed":executed,"sanity_check":sanity}
    finish = recipe.get("ui_finish", {}) or {}
    result["next_ui"] = finish
    return result
