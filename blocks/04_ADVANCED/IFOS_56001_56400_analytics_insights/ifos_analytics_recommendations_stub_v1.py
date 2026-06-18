# ifos_analytics_recommendations_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def recommend(metrics: Dict, signals: Dict) -> List[Dict]:
    out=[]
    if metrics.get("error_rate",0) > 0.02:
        out.append({"type":"reliability","summary":"High error_rate -> add retries/cache","priority":"high"})
    return out
