# ifos_fetcher_stub_v1.py
from __future__ import annotations
import hashlib, requests

def fetch(url: str) -> dict:
    r=requests.get(url, timeout=20)
    b=r.content
    return {"status": r.status_code, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
