# IFOS Runtime Engine Skeleton v1
# Executes a recipe as a job-run with adapters, state store, secret vault, sandbox policy.
# NOTE: MVP skeleton for architecture; replace stubs with real implementations.

from __future__ import annotations
import json, time, hashlib, datetime
from typing import Dict, Any, Optional, List, Tuple

class StateStore:
    def get(self, job_id: str, key: str) -> Any: raise NotImplementedError
    def set(self, job_id: str, key: str, value: Any) -> None: raise NotImplementedError
    def compare_and_set(self, job_id: str, key: str, expected: Any, new: Any) -> bool: raise NotImplementedError

class InMemoryStateStore(StateStore):
    def __init__(self):
        self._d: Dict[Tuple[str,str], Any] = {}
    def get(self, job_id: str, key: str) -> Any:
        return self._d.get((job_id,key))
    def set(self, job_id: str, key: str, value: Any) -> None:
        self._d[(job_id,key)] = value
    def compare_and_set(self, job_id: str, key: str, expected: Any, new: Any) -> bool:
        cur = self._d.get((job_id,key))
        if cur != expected: return False
        self._d[(job_id,key)] = new
        return True

class SecretVault:
    def get(self, secret_ref: str, ctx: Dict[str, Any]) -> str: raise NotImplementedError

class EnvSecretVault(SecretVault):
    # MVP: maps vault refs to ENV keys via metadata (stub)
    def __init__(self, mapping: Dict[str,str]):
        self.mapping = mapping
    def get(self, secret_ref: str, ctx: Dict[str, Any]) -> str:
        import os
        env_key = self.mapping.get(secret_ref,"")
        if not env_key:
            raise RuntimeError(f"No mapping for secret_ref: {secret_ref}")
        val = os.getenv(env_key,"")
        if not val:
            raise RuntimeError(f"Missing env secret: {env_key}")
        return val

class SandboxPolicy:
    def __init__(self, policy: Dict[str, Any]):
        self.allow_hosts = set(policy.get("allow_hosts", []))
        self.deny_methods = set(policy.get("deny_methods", ["DELETE","PUT","PATCH"]))
        self.max_requests = int(policy.get("max_requests_per_run", 50))
        self.max_run_runtime_sec = int(policy.get("max_run_runtime_sec", 300))

class AdapterContext:
    def __init__(self, mode: str, sandbox: Optional[SandboxPolicy], secrets: Dict[str,str], state: StateStore, job_id: str, trace_id: str):
        self.mode = mode
        self.sandbox = sandbox
        self.secrets = secrets
        self.state = state
        self.job_id = job_id
        self.trace_id = trace_id

class Adapter:
    def validate(self, params: Dict[str, Any]) -> List[str]: return []
    def execute(self, params: Dict[str, Any], ctx: AdapterContext) -> Dict[str, Any]: raise NotImplementedError
    def redact(self, obj: Any) -> Any: return obj

class AdapterRegistry:
    def __init__(self):
        self._m: Dict[str, Adapter] = {}
    def register(self, function_id: str, adapter: Adapter) -> None:
        self._m[function_id] = adapter
    def get(self, function_id: str) -> Adapter:
        if function_id not in self._m:
            raise KeyError(f"Adapter not found for function_id={function_id}")
        return self._m[function_id]

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def run_recipe(job: Dict[str, Any], recipe: Dict[str, Any], registry: AdapterRegistry, state: StateStore, vault: SecretVault) -> Dict[str, Any]:
    started = datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"
    trace_id = "trace_" + sha256_bytes((job["job_id"]+started).encode())[:12]

    mode = job.get("mode","dry_run")
    sandbox = SandboxPolicy(job.get("sandbox_policy", {})) if mode in ("sandbox","dry_run") else None

    # resolve secrets into values (only now)
    secrets_map: Dict[str,str] = {}
    for k, ref in (job.get("secrets") or {}).items():
        if mode == "dry_run":
            # dry-run should not fetch real secrets; use placeholder
            secrets_map[k] = "REDACTED_DRY_RUN"
        else:
            secrets_map[k] = vault.get(ref, {"job_id": job["job_id"], "trace_id": trace_id})

    ctx = AdapterContext(mode=mode, sandbox=sandbox, secrets=secrets_map, state=state, job_id=job["job_id"], trace_id=trace_id)

    run_steps = []
    artifacts = []
    status = "PASS"
    request_count = 0
    t0 = time.time()

    for step in recipe.get("steps", []):
        step_id = step["id"]
        kind = step["kind"]
        s_started = time.time()
        srec = {"step_id": step_id, "kind": kind, "status": "PASS", "started_at": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"}

        try:
            if kind == "action":
                function_id = step.get("uses","")
                adapter = registry.get(function_id)

                # sandbox request budget
                request_count += 1
                if sandbox and request_count > sandbox.max_requests:
                    raise RuntimeError("Sandbox max_requests_per_run exceeded")

                # basic param binding (MVP): allow literal values only; real engine would resolve templates
                params = step.get("in") or {}
                # inject inputs if present in job (simplified)
                # NOTE: real engine resolves {{inputs.x}} etc.
                for key, val in list(params.items()):
                    if isinstance(val, str) and val.startswith("{{inputs.") and val.endswith("}}"):
                        ik = val[len("{{inputs."):-2]
                        params[key] = job.get("inputs", {}).get(ik)

                errs = adapter.validate(params)
                if errs:
                    srec["status"] = "FAIL"
                    srec["error"] = {"type":"validation", "errors": errs}
                    status = "FAIL"
                else:
                    res = adapter.execute(params, ctx)
                    srec["uses"] = function_id
                    srec["request_redacted"] = adapter.redact(params)
                    srec["response_redacted"] = adapter.redact(res)

            elif kind in ("transform","filter","store","foreach","rate_limit"):
                # MVP: not implemented fully
                srec["status"] = "WARN"
                srec["response_redacted"] = {"note":"Not implemented in skeleton; handle in real engine."}
                if status != "FAIL":
                    status = "WARN"
            else:
                srec["status"] = "WARN"
                srec["response_redacted"] = {"note":"Unknown step kind"}
                if status != "FAIL":
                    status = "WARN"

        except Exception as e:
            srec["status"] = "FAIL"
            srec["error"] = {"type":"exception", "message": str(e)}
            status = "FAIL"

        srec["finished_at"] = datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"
        srec["duration_ms"] = int((time.time() - s_started)*1000)
        run_steps.append(srec)

        # runtime budget
        if sandbox and (time.time() - t0) > sandbox.max_run_runtime_sec:
            status = "FAIL"
            run_steps.append({"step_id":"_runtime_budget","kind":"guard","status":"FAIL",
                              "started_at": srec["finished_at"], "finished_at": srec["finished_at"],
                              "duration_ms":0, "error":{"type":"budget","message":"max_run_runtime_sec exceeded"}})
            break

    # artifact example: run log JSON (redacted already)
    run_obj = {
        "run_id": f"run.{job['job_id']}.1",
        "job_id": job["job_id"],
        "attempt": 1,
        "started_at": started,
        "finished_at": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z",
        "status": status,
        "mode": mode,
        "policy": {"redaction_applied": True, "pii": False, "money": False, "security_sensitive": False},
        "steps": run_steps,
        "artifacts": [],
        "state_updates": [],
        "notes": "Skeleton run record."
    }
    payload = json.dumps(run_obj, ensure_ascii=False, indent=2).encode("utf-8")
    run_sha = sha256_bytes(payload)
    artifacts.append({"name":"run_log.json","sha256":run_sha,"uri":"artifact://local/run_log.json","redacted":True})
    run_obj["artifacts"] = artifacts
    return run_obj
