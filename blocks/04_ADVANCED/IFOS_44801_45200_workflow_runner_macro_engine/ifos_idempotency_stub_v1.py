# ifos_idempotency_stub_v1.py
from __future__ import annotations

_seen=set()

def check_and_mark(key: str) -> bool:
    if key in _seen:
        return False
    _seen.add(key)
    return True
