# ifos_signing_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def sign_payload(payload_hash: str, key_ref: str, alg: str = "ed25519") -> Dict[str, Any]:
    return {"alg": alg, "key_ref": key_ref, "payload_hash": payload_hash, "signature":"<stub>"}
