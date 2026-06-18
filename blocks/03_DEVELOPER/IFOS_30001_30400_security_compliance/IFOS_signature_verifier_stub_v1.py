# IFOS Signature Verifier Stub v1
from __future__ import annotations
from typing import Dict, Any

def verify(signature_obj: Dict[str, Any], expected_hash: str) -> bool:
    # Stub: in real life verify crypto signature
    return signature_obj.get("package_hash") == expected_hash
