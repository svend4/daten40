# IFOS Payment Webhook Handler Stub v1
from __future__ import annotations
from typing import Dict, Any
import hmac, hashlib

def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    sig=hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(sig, signature)

def handle_event(event: Dict[str, Any]) -> str:
    # Placeholder routing; real system maps provider event types -> order updates
    et=event.get("type","")
    if "succeeded" in et:
        return "payment_succeeded"
    if "failed" in et:
        return "payment_failed"
    return "ignored"
