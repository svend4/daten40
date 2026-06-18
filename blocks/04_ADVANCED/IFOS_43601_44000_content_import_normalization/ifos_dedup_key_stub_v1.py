# ifos_dedup_key_stub_v1.py
from __future__ import annotations
import hashlib

def exact_hash(title: str, body: str, source: str) -> str:
    s=(title.strip()+"\n"+body.strip()+"\n"+source).encode("utf-8")
    return "sha256:"+hashlib.sha256(s).hexdigest()
