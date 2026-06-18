# ifos_process_simulator_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def simulate(process: Dict[str,Any], event: Dict[str,Any]) -> Dict[str,Any]:
    # Very naive simulator: just returns steps in order
    return {"process_id": process.get("process_id"), "steps":[s.get("step_id") for s in process.get("steps",[])]}
