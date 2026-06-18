# ifos_signing_stub_v1.py
from __future__ import annotations
from typing import Dict

def sign(artifact_digest: str, method: str="sigstore") -> Dict:
    return {"method":method,"digest":artifact_digest,"issuer":"ifos-ci","ts":"now","version":"1.0.0"}
