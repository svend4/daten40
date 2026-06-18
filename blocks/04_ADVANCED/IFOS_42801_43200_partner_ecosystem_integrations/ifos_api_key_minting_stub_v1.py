# ifos_api_key_minting_stub_v1.py
from __future__ import annotations
import secrets

def mint(prefix: str="key") -> str:
    return f"{prefix}_" + secrets.token_urlsafe(24)
