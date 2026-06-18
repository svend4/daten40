# ifos_vault_signature_stub_v1.py
from __future__ import annotations
import hmac, hashlib

def sign_hmac(key: bytes, payload: bytes) -> str:
    return hmac.new(key, payload, hashlib.sha256).hexdigest()
