# IFOS Entitlement Engine Stub v1
from __future__ import annotations
from typing import Dict, Any, Optional
import datetime, json, base64, hmac, hashlib

def sign_blob(data: Dict[str, Any], secret: str) -> Dict[str, str]:
    payload=json.dumps(data, separators=(",",":"), ensure_ascii=False).encode("utf-8")
    sig=hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return {"payload_b64": base64.urlsafe_b64encode(payload).decode("utf-8"), "signature": sig}

def verify_blob(payload_b64: str, signature: str, secret: str) -> bool:
    payload=base64.urlsafe_b64decode(payload_b64.encode("utf-8"))
    sig=hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(sig, signature)

def is_entitlement_active(ent: Dict[str, Any], now: Optional[str]=None) -> bool:
    if ent.get("status") != "active":
        return False
    exp=ent.get("expires_at")
    if not exp:
        return True
    dt=datetime.datetime.fromisoformat(exp.replace("Z","+00:00"))
    cur=datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    return cur <= dt
