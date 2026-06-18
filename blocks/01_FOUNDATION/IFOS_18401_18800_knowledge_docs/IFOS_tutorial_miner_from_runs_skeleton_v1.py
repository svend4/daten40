# IFOS Tutorial Miner from Runs Skeleton v1
from __future__ import annotations
from typing import Dict, Any, Tuple

def sanitize_run(run: Dict[str, Any]) -> Dict[str, Any]:
    # Stub: remove secrets + redact PII
    r = dict(run)
    r["secrets_removed"] = True
    r["pii_redacted"] = True
    return r

def mine_tutorial_from_run(run: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    r = sanitize_run(run)
    steps = []
    for i,evt in enumerate(r.get("major_events",[]) or [], start=1):
        steps.append({"id":str(i),"title":evt.get("title","Step"),"do":evt.get("do",""),"check":evt.get("check",""),"notes":evt.get("notes","")})
    tutorial = {
        "tutorial_id":"tut.mined",
        "title":"Mined tutorial",
        "goal":"Derived from successful run",
        "steps":steps,
        "expected_result":"PASS",
        "refs":[r.get("run_id","")],
        "version":"1.0.0",
        "updated_at":""
    }
    mapping = {"map_id":"map.mined","run_id":r.get("run_id",""),"tutorial_id":"tut.mined","sanitization":{"pii_redacted":True,"secrets_removed":True,"notes":""},"evidence_refs":[r.get("evidence_ref","")],"version":"1.0.0","updated_at":""}
    return tutorial, mapping
