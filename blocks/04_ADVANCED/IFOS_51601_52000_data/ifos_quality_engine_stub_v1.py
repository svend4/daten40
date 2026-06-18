# ifos_quality_engine_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def score(payload: Dict, errors: List[str]) -> float:
    base=1.0
    penalty=min(0.9, 0.1*len(errors))
    return max(0.0, base-penalty)
