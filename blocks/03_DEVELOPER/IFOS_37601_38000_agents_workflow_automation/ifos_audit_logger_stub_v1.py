# ifos_audit_logger_stub_v1.py
from __future__ import annotations
from typing import Dict, Any
import json, time

def write_audit(event: Dict[str, Any], path: str = "audit.log") -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
