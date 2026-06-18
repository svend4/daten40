# ifos_oneclick_planner_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def plan(manifest: Dict) -> Dict:
    steps=[]
    for item in manifest.get("items",[]):
        steps.append({"op":"install_item","item":item})
    steps.append({"op":"smoke_tests"})
    return {"steps":steps,"checkpoints":["after_install"],"notes":["stub"]}
