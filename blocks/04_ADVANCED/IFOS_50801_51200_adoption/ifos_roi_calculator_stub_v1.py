# ifos_roi_calculator_stub_v1.py
from __future__ import annotations
from typing import Dict

def compute(baseline: Dict, after: Dict, costs: Dict) -> Dict:
    # naive example: save minutes per unit
    saved = max(0, baseline.get("minutes_per_ticket",0) - after.get("minutes_per_ticket",0))
    per_week = saved * baseline.get("tickets_per_week",0) / 60.0
    return {"saved_hours_week": per_week, "costs": costs}
