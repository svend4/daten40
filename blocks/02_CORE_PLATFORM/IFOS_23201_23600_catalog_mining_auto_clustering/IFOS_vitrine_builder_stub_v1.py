# IFOS Vitrine Builder Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def build_vitrine(cluster: Dict[str, Any], atoms: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Stub: create simple vitrine with cards per atom
    cards=[]
    for a in atoms:
        cards.append({"title":a.get("title",""),"bullets":[a.get("action","")], "evidence":a.get("sources",[]), "risk":"unknown"})
    return {"vitrine_id":"vit.demo","cluster_id":cluster["cluster_id"],"headline":cluster["name"],"cards":cards,"cta":{}, "updated_at":"", "version":"1.0.0"}
