# ifos_community_reputation_scoring_stub_v1.py
from __future__ import annotations
from typing import Dict

def score(signals: Dict) -> Dict:
    # Placeholder scoring: weighted sum
    installs = signals.get("installs",0)
    runs = signals.get("verified_runs",0)
    refunds = signals.get("refunds",0)
    complaints = signals.get("complaints",0)
    s = installs*0.1 + runs*0.2 - refunds*1.0 - complaints*2.0
    level = "new"
    if s > 50: level = "trusted"
    if s > 200: level = "maintainer"
    if s > 500: level = "partner"
    return {"score": s, "level": level}
