# ifos_reputation_engine_stub_v1.py
from __future__ import annotations
from typing import Dict

def update(rep: Dict, delta: float) -> Dict:
    rep["score"]=max(0,min(100,rep.get("score",50)+delta))
    return rep
