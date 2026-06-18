# IFOS Receipt Emitter Stub v1
from __future__ import annotations
from typing import Dict, Any
import hashlib, json

def sign_receipt(receipt: Dict[str, Any]) -> Dict[str, Any]:
    b = json.dumps(receipt, sort_keys=True, ensure_ascii=False).encode("utf-8")
    receipt["signature"] = "sha256:" + hashlib.sha256(b).hexdigest()
    return receipt
