# ifos_record_replay_stub_v1.py
from __future__ import annotations
from typing import Dict

def record(session: Dict) -> Dict:
    # Store sanitized records
    return {"session_id": session.get("session_id","rr.new"), "count": len(session.get("records",[]))}
