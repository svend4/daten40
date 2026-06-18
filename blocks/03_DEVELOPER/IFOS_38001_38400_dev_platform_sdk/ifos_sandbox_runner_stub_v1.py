# ifos_sandbox_runner_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def start(env: Dict[str, Any]) -> Dict[str, Any]:
    return {"status":"started","endpoints":env.get("endpoints",{})}
