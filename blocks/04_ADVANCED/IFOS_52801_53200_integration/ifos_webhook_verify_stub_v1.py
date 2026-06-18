# ifos_webhook_verify_stub_v1.py
from __future__ import annotations
import hmac, hashlib
from typing import Dict

def verify(secret: bytes, payload: bytes, signature: str) -> bool:
    mac=hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, signature)
