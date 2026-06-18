# IFOS Install Planner Stub v1
from __future__ import annotations
from typing import Dict, Any
import hashlib, json

def plan_install(install_request: Dict[str, Any]) -> Dict[str, Any]:
    # Create a deterministic plan skeleton + lock hash placeholder.
    lock = {"resolved": install_request.get("pinned_versions", {}), "subject_id": install_request["subject_id"]}
    lock_hash = "sha256:" + hashlib.sha256(json.dumps(lock, sort_keys=True).encode("utf-8")).hexdigest()
    steps = ["resolve_deps","lock_versions","request_permissions","request_secrets","apply_migrations","install_artifacts","configure_runtime","health_checks","write_receipt"]
    return {"plan_id":"plan.demo","request_id":install_request["request_id"],"steps":[{"name":s,"status":"planned"} for s in steps],"lockfile_hash":lock_hash}
