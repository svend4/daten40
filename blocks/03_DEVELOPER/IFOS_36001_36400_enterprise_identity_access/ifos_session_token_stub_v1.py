# ifos_session_token_stub_v1.py
from __future__ import annotations
from typing import Dict, Any
import time, hmac, hashlib, base64, json

def sign(payload: Dict[str, Any], secret: str) -> str:
    body=json.dumps(payload,separators=(",",":"),ensure_ascii=False).encode("utf-8")
    sig=hmac.new(secret.encode("utf-8"), body, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(body).decode()+"."+base64.urlsafe_b64encode(sig).decode()

def verify(token: str, secret: str) -> bool:
    try:
        b64, s64 = token.split(".",1)
        body=base64.urlsafe_b64decode(b64.encode())
        sig=base64.urlsafe_b64decode(s64.encode())
        exp=hmac.new(secret.encode(), body, hashlib.sha256).digest()
        return hmac.compare_digest(sig, exp)
    except Exception:
        return False
