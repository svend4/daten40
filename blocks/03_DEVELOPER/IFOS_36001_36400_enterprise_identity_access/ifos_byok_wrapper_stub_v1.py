# ifos_byok_wrapper_stub_v1.py
from __future__ import annotations
from typing import Dict

def envelope_encrypt(plaintext: bytes, key_ref: str, context: Dict[str,str]) -> bytes:
    # Stub: real implementation would call KMS/HSM.
    return b"enc:" + plaintext
