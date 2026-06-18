# ifos_audit_logger_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def log(event: Dict[str, Any]) -> None:
    # Stub: print to stdout (real impl would append to WORM storage)
    print("AUDIT", event.get("action"), event.get("result"))
