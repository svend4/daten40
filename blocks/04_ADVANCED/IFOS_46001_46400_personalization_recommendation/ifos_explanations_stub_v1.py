# ifos_explanations_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def explain(item: Dict, context: Dict) -> List[str]:
    reasons=[]
    if context.get("intent"):
        reasons.append("подходит под intent: "+str(context["intent"]))
    if item.get("trust_tier"):
        reasons.append("уровень доверия: "+str(item["trust_tier"]))
    if item.get("setup_minutes") is not None:
        reasons.append("оценка времени настройки: %s мин" % item["setup_minutes"])
    return reasons[:4]
