# ifos_audit_logger_stub_v1.py
from __future__ import annotations
from typing import Dict

def log(action: str, target: Dict, actor: Dict, reason: str="") -> Dict:
    return {"action":action,"target":target,"actor":actor,"reason":reason}
