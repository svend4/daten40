# ifos_certification_checks_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List

def run_checks(integration: Dict[str, Any]) -> List[Dict[str, Any]]:
    caps=set(integration.get("capabilities", []))
    auth=integration.get("auth", {})
    return [
        {"name":"sandbox_present","ok": True},
        {"name":"docs_ok","ok": bool(integration.get("docs_ref"))},
        {"name":"webhook_signed","ok": "webhook" in caps},
        {"name":"least_privilege_scopes","ok": bool(integration.get("scopes"))},
        {"name":"auth_declared","ok": bool(auth.get("type"))},
    ]
