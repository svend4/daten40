# ifos_runner_stub_v1.py
from __future__ import annotations
from typing import Dict

def execute_dag(dag: Dict, params: Dict) -> Dict:
    executed=[]
    for n in dag.get("nodes", []):
        executed.append({"task_id": n.get("id"), "op": n.get("op"), "status":"done"})
    return {"status":"done","executed":executed,"artifacts":[]}
