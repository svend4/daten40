# IFOS Sandbox Manager Stub v1
from __future__ import annotations
from typing import Dict, Any

def start_session(profile_id: str) -> Dict[str, Any]:
    return {"session_id":"sb.demo","profile_id":profile_id,"status":"running"}

def stop_session(session_id: str) -> Dict[str, Any]:
    return {"session_id":session_id,"status":"stopped"}
