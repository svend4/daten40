# ifos_compare_panel_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def compare(items: List[Dict], criteria: List[Dict]) -> Dict:
    # stub: returns items with placeholder scores
    out=[]
    for it in items:
        out.append({"item":it, "score":0.5})
    return {"rows":out, "verdict":"depends on priority"}
