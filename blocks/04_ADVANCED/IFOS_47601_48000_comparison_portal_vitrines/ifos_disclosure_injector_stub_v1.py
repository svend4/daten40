# ifos_disclosure_injector_stub_v1.py
from __future__ import annotations
from typing import Dict

def inject(view: Dict, disclosure: Dict) -> Dict:
    view["disclosure"]=disclosure
    return view
