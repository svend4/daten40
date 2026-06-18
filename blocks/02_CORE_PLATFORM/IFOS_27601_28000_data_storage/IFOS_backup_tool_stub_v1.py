# IFOS Backup Tool Stub v1
from __future__ import annotations
from typing import Dict, Any, List
import hashlib

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def build_manifest(files: Dict[str, bytes]) -> Dict[str, Any]:
    entries = []
    for path, data in files.items():
        entries.append({"path": path, "sha256": sha256_bytes(data), "size_bytes": len(data)})
    return {"kind":"backup_snapshot","entries":entries}
