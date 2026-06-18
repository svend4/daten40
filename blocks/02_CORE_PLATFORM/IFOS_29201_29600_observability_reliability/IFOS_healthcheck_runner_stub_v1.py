# IFOS Healthcheck Runner Stub v1
from __future__ import annotations
from typing import Dict, Any

def run_check(check: Dict[str, Any], env: Dict[str, Any]) -> Dict[str, Any]:
    kind = check.get("kind")
    details = {}
    status = "ok"
    if kind == "secret":
        missing = []
        required = env.get("required_secret_refs", []) or []
        present = set(env.get("present_secret_refs", []) or [])
        for r in required:
            if r not in present:
                missing.append(r)
        if missing:
            status = "broken"
            details["missing"] = missing
    return {"ts": env.get("ts"), "status": status, "details": details}
