# IFOS Rollback Manager Stub v1
from __future__ import annotations
from typing import Dict, Any, List

class RollbackManager:
    def execute(self, plan: Dict[str, Any]) -> List[str]:
        steps=plan.get("steps", [])
        executed=[]
        for s in steps:
            executed.append(s.get("op","unknown"))
        return executed
