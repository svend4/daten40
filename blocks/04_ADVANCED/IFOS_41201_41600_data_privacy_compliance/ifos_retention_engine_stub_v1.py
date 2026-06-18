# ifos_retention_engine_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List

def evaluate(objects: List[Dict[str, Any]], policy: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Stub: return actions for objects based on class match (real: age calculation, holds)
    rules=policy.get("rules",[])
    actions=[]
    for obj in objects:
        cls=obj.get("class")
        for r in rules:
            if r.get("class")==cls:
                actions.append({"object":obj.get("id"),"action":r.get("action")})
                break
    return actions
