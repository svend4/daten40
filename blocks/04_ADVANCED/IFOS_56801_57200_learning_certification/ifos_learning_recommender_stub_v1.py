# ifos_learning_recommender_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def recommend(user_stats: Dict) -> List[str]:
    out=[]
    if user_stats.get("auth_errors",0) > 3:
        out.append("lesson.oauth_basics")
    if user_stats.get("dropoff_step2",0) > 5:
        out.append("lesson.workflow_step2_fix")
    return out
