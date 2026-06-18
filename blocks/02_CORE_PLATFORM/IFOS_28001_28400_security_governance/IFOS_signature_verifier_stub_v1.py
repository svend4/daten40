# IFOS Signature Verifier Stub v1
from __future__ import annotations
from typing import Dict, Any

def verify_manifest(manifest_sha256: str, signature_obj: Dict[str, Any], trusted_signers: Dict[str, str]) -> Dict[str, Any]:
    """Stub: checks signer_id is trusted. Real implementation verifies crypto signature."""
    signer = signature_obj.get("signer_id","")
    if signer not in trusted_signers:
        return {"ok": False, "reason": "untrusted_signer", "signer_id": signer}
    # TODO: cryptographic verification (ed25519/ecdsa)
    return {"ok": True, "reason": "trusted_signer_stub", "signer_id": signer}
