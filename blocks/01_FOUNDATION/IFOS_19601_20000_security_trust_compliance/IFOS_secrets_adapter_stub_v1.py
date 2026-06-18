# IFOS Secrets Adapter Stub v1
from __future__ import annotations
from typing import Dict, Any
import time

def resolve_secret(secret_ref: str, scope_id: str) -> Dict[str, Any]:
    # Return time-limited handle, not raw secret
    return {"secret_ref": secret_ref, "handle": "handle:"+secret_ref, "expires_at": time.time()+300}
