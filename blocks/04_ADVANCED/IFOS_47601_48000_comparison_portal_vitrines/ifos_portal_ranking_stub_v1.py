# ifos_portal_ranking_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def build_ranking(scored: List[Dict]) -> Dict:
    return {"top": scored[:10], "count": len(scored)}
