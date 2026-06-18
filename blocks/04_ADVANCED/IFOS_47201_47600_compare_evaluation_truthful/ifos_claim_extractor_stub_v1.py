# ifos_claim_extractor_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def extract_claims(item: Dict) -> List[Dict]:
    # stub: returns one claim from title
    title=item.get("title","")
    return [{"claim_text": title, "type":"unknown"}] if title else []
