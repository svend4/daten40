# IFOS Orchestrator Skeleton v1
# Coordinates validation -> secrets -> sandbox -> target adapter -> run record.
from __future__ import annotations
from typing import Dict, Any
import time
import uuid

class Orchestrator:
    def __init__(self, sandbox, secret_resolver, target_adapters: Dict[str, Any], store: Any):
        self.sandbox = sandbox
        self.secret_resolver = secret_resolver
        self.target_adapters = target_adapters
        self.store = store  # persistence interface

    def trigger_run(self, job: Dict[str, Any]) -> Dict[str, Any]:
        run_id = f"run.{uuid.uuid4().hex[:10]}"
        started = time.time()

        # 1) Validate policy/flags/contracts (stub)
        self.sandbox.precheck(job)

        # 2) Resolve secrets ephemerally
        secrets = self.secret_resolver.resolve(job["tenant_id"], job.get("secrets", []))

        # 3) Dispatch to target adapter
        target = job["target"]
        adapter = self.target_adapters[target]
        result = adapter.run(job, secrets)

        # 4) Collect outputs/metrics and redact
        logs = result.get("logs", "")
        logs = self.sandbox.redact(logs, secrets)

        finished = time.time()
        run = {
            "run_id": run_id,
            "job_id": job["job_id"],
            "status": result.get("status", "success"),
            "started_at": started,
            "finished_at": finished,
            "metrics": result.get("metrics", {}),
            "logs": logs,
            "artifacts": result.get("artifacts", []),
        }

        # 5) Persist
        self.store.save_run(run)
        return run
