# ifos_partner_risk_score_stub_v1.py
from __future__ import annotations
from typing import List, Dict, Any

WEIGHTS={"bot_traffic":0.4,"geo_mismatch":0.2,"refund_abuse":0.3,"chargeback_spike":0.5,"fake_installs":0.4,"other":0.1}

def score(signals: List[Dict[str, Any]]) -> float:
    s=0.0
    for sig in signals:
        t=sig.get("type","other")
        sev=sig.get("severity","low")
        mult={"low":0.25,"medium":0.5,"high":0.8,"critical":1.0}.get(sev,0.25)
        s += WEIGHTS.get(t,0.1)*mult
    return min(1.0, s)
