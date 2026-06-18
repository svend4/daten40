# ifos_idempotency_key_stub_v1.py
from __future__ import annotations
import hashlib, json
from typing import Dict, Any

def make_idempotency_key(tenant_id: str, asset: Dict[str, Any], inputs: Dict[str, Any]) -> str:
    payload={"tenant_id":tenant_id,"asset":asset,"inputs":inputs}
    h=hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    return "idem:"+h
