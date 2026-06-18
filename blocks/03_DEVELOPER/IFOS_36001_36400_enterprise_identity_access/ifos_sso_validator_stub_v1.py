# ifos_sso_validator_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def validate_oidc(claims: Dict[str, Any], domain_allowlist: list[str]) -> bool:
    email=claims.get("email","")
    domain=email.split("@")[-1] if "@" in email else ""
    return domain in domain_allowlist
