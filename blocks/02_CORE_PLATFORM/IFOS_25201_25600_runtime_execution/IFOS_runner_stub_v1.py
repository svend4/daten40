# IFOS Runner Stub v1
from __future__ import annotations
from typing import Dict, Any, List
import time, hashlib, json

def _sha(obj: Any) -> str:
    b = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(b).hexdigest()

def run_plan(plan: Dict[str, Any], profile: Dict[str, Any], secrets: Dict[str, str]) -> Dict[str, Any]:
    start = time.time()
    steps_out=[]
    for step in plan.get("steps", []):
        n=step["n"]
        # Stub: pretend each step succeeds, except if allow_external=False in prod.
        if plan.get("mode")=="prod" and step.get("allow_external") is False:
            steps_out.append({"n":n,"status":"fail","error":"external not allowed"})
            break
        steps_out.append({"n":n,"status":"pass","retries":0,"external_calls":[]})
    result = "success" if all(s["status"]=="pass" for s in steps_out) else "failure"
    dur_ms=int((time.time()-start)*1000)
    receipt={
        "receipt_id":"rcpt.demo",
        "job_id":"job.demo",
        "subject_id":plan.get("subject_id",""),
        "mode":plan.get("mode","sandbox"),
        "inputs_redacted":{},
        "outputs_redacted":{},
        "steps":steps_out,
        "result":result,
        "duration_ms":dur_ms,
        "cost_estimate":{"usd":0.0},
        "hashes":{"plan_hash":_sha(plan), "inputs_hash":_sha({}), "outputs_hash":_sha({})},
        "created_at":"",
        "updated_at":"",
        "version":"1.0.0"
    }
    return receipt
