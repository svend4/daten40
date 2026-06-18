# ifos_evidence_matcher_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def bind_evidence(claims: List[Dict], item: Dict) -> List[Dict]:
    # stub: attaches canonical url as evidence
    url=item.get("canonical_url")
    for c in claims:
        c["evidence"]=[{"url":url,"snippet":"(placeholder)"}] if url else []
    return claims
