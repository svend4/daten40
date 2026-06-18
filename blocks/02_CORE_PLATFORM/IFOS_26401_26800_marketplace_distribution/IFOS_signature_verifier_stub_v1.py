# IFOS Signature Verifier Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def verify_signature(signature_obj: Dict[str, Any], hashes: List[str], trust_store: Dict[str, Any]) -> bool:
    """Stub: checks signer is known and hashes match list; does NOT cryptographically verify."""
    signer = signature_obj.get("signer_id")
    if signer not in trust_store.get("allowed_signers", []):
        return False
    signed = set(signature_obj.get("signed_hashes", []))
    return set(hashes).issubset(signed)
