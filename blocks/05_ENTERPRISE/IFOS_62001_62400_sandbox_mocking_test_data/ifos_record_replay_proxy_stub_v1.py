# ifos_record_replay_proxy_stub_v1.py
from __future__ import annotations
from typing import Dict, Any
import hashlib, json

def redact(entry: Dict[str, Any]) -> Dict[str, Any]:
    # placeholder: remove obvious PII fields
    e = json.loads(json.dumps(entry))
    for k in ["email","phone","address"]:
        if k in e.get("response", {}).get("body", {}):
            e["response"]["body"][k] = "***"
    return e

def sign(recording: Dict[str, Any]) -> str:
    b = json.dumps(recording, sort_keys=True).encode("utf-8")
    return hashlib.sha256(b).hexdigest()
