# ifos_triage_bot_stub_v1.py
from __future__ import annotations
from typing import Dict

KNOWN = {"401":"re-auth connector", "429":"add backoff", "timeout":"check network"}

def triage(error_code: str) -> Dict:
    return {"classification":"known_issue" if error_code in KNOWN else "unknown",
            "action": KNOWN.get(error_code,"collect diagnostics")}
