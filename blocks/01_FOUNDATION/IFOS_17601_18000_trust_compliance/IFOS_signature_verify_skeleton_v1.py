# IFOS Signature Verify Skeleton v1
from __future__ import annotations
from typing import Dict, Any
import hashlib, base64

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def verify_signature(envelope: Dict[str, Any], public_key_pem: str) -> bool:
    # Stub: real impl depends on algorithm (ed25519/rsa/etc).
    # Here we only check envelope completeness.
    required = ["subject_hash","signature","algorithm","signer"]
    return all(k in envelope for k in required)
