# ifos_ab_assignment_stub_v1.py
from __future__ import annotations
import hashlib
from typing import Dict, Any, List

def assign(subject_key: str, variants: List[Dict[str, Any]], salt: str = "ifos") -> str:
    # Deterministic: hash(subject_key+salt) -> bucket -> variant by weight
    h = hashlib.sha256((subject_key + "|" + salt).encode("utf-8")).hexdigest()
    bucket = int(h[:8], 16) / 0xFFFFFFFF
    acc = 0.0
    for v in variants:
        acc += float(v.get("weight", 0.0))
        if bucket <= acc:
            return v["variant_id"]
    return variants[-1]["variant_id"]
