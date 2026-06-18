# IFOS Signature Verify Stub v1
from __future__ import annotations
from typing import Dict, Any

def verify_signature(signature: Dict[str, Any], expected_hash: str, key: Dict[str, Any]) -> bool:
    # Placeholder: integrate with real crypto lib (ed25519/rsa/ecdsa)
    if signature.get("hash") != expected_hash:
        return False
    if key.get("status") != "active":
        return False
    return True
