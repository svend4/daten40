# ifos_review_moderator_stub_v1.py
from __future__ import annotations
from typing import Dict

def moderate(review: Dict) -> Dict:
    # stub: always publish
    return {"decision":"publish","reasons":["stub"],"redactions":[]}
