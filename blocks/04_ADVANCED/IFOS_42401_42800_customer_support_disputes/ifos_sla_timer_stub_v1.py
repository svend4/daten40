# ifos_sla_timer_stub_v1.py
from __future__ import annotations
from datetime import datetime, timedelta
from typing import Dict, Any

def compute_deadlines(opened_at: str, policy: Dict[str, Any]) -> Dict[str, str]:
    t=datetime.fromisoformat(opened_at.replace("Z",""))
    frt=timedelta(minutes=int(policy.get("targets",{}).get("FRT_minutes",60)))
    ttr=timedelta(hours=int(policy.get("targets",{}).get("TTR_hours",24)))
    return {"frt_deadline": (t+frt).isoformat()+"Z", "ttr_deadline": (t+ttr).isoformat()+"Z"}
