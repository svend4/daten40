# ifos_offline_snapshot_packer_stub_v1.py
from __future__ import annotations
from typing import Dict, Any
import json, hashlib

def make_manifest(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    b=json.dumps(snapshot, sort_keys=True).encode("utf-8")
    return {"snapshot_id": snapshot.get("snapshot_id"), "hash":"sha256:"+hashlib.sha256(b).hexdigest()}
