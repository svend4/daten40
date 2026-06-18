# ifos_rollout_planner_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def make_canary_plan(artifacts: List[str]) -> Dict:
    return {
        "plan_id":"rpl.generated",
        "artifact_set": artifacts,
        "strategy":"canary",
        "stages":[
            {"name":"pilot","percent":1,"gates":["docs_ready","benchmarks_passed"]},
            {"name":"canary","percent":10,"gates":["owner_approval"]},
            {"name":"full","percent":100,"gates":["slo_ok"]},
        ],
        "rollback":["instant_rollback"],
        "version":"1.0.0"
    }
