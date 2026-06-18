# ifos_snapshotter_stub_v1.py
from __future__ import annotations
import json, hashlib
from typing import Dict, Any

def snapshot(obj: Dict[str,Any]) -> str:
    b=json.dumps(obj, sort_keys=True).encode("utf-8")
    return "sha256:"+hashlib.sha256(b).hexdigest()
