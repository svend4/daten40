# ifos_conference_agenda_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def agenda(clusters: List[Dict]) -> Dict:
    return {"sections":[{"title":"Top clusters","items":[c.get("cluster_id") for c in clusters[:10]]}],
            "decisions":[], "actions":[]}
