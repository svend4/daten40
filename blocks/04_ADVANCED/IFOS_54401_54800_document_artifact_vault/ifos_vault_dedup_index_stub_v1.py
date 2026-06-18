# ifos_vault_dedup_index_stub_v1.py
from __future__ import annotations
from typing import Dict

DEDUP: Dict[str, str] = {}  # content_hash -> storage_path

def put(content_hash: str, storage_path: str) -> None:
    DEDUP[content_hash] = storage_path
