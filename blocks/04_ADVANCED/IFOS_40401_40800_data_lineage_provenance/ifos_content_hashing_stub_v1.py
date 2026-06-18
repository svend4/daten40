# ifos_content_hashing_stub_v1.py
from __future__ import annotations
import hashlib

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
