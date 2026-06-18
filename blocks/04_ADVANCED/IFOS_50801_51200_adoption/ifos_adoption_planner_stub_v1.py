# ifos_adoption_planner_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def plan(org: Dict, packs: List[str]) -> Dict:
    return {"org_id": org["org_id"], "phases":["pilot","team","org"], "template_packs": packs}
