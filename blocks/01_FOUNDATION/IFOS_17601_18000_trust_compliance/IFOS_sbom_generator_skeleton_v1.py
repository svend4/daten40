# IFOS SBOM Generator Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List
import hashlib, json

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def generate_sbom(subject: Dict[str, Any], components: List[Dict[str, Any]], fmt: str="ifos-min") -> Dict[str, Any]:
    # In real system: resolve deps from lockfiles, containers, plugin manifests.
    return {
        "sbom_id":"sbom.generated",
        "subject":subject,
        "format":fmt,
        "components":components,
        "generated_at":"",
        "version":"1.0.0"
    }

def sbom_hash(sbom: Dict[str, Any]) -> str:
    return sha256_bytes(json.dumps(sbom, sort_keys=True).encode("utf-8"))
