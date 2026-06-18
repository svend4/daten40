# IFOS Runner Orchestrator Stub v1
from __future__ import annotations
from typing import Dict, Any, Optional
import time

class Runner:
    def __init__(self, policy_eval, secrets_mgr, logs) -> None:
        self.policy_eval = policy_eval
        self.secrets_mgr = secrets_mgr
        self.logs = logs

    def run(self, req: Dict[str, Any]) -> Dict[str, Any]:
        run_id=req["run_id"]
        self.logs.info(run_id, "run_received", {"target": req.get("target_id")})
        decision=self.policy_eval.evaluate(req)
        if decision["allowed"] is False:
            self.logs.warn(run_id, "policy_denied", {"reason": decision.get("reason")})
            return {"run_id": run_id, "status": "failed", "error": {"kind":"policy","reason": decision.get("reason")}}
        bindings=req.get("secrets", [])
        injected=self.secrets_mgr.prepare(bindings)
        self.logs.info(run_id, "secrets_bound", {"count": len(injected)})
        # simulated execution
        time.sleep(0.01)
        self.logs.info(run_id, "run_finished", {"exit_code": 0})
        return {"run_id": run_id, "status": "succeeded", "exit_code": 0, "outputs": {}}
