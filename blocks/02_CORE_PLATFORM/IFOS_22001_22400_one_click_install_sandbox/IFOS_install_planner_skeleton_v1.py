# IFOS Install Planner Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List

STEP_ORDER = [
    "fetch_payload","verify_signatures","verify_sbom","apply_policy_precheck",
    "install_plugin","import_workflow","import_flow","configure_credentials",
    "configure_webhooks","run_migrations","run_smoke_tests","promote_to_prod"
]

def build_plan(subject: Dict[str, Any], target_platform: str, mode: str, deps: List[str]) -> Dict[str, Any]:
    # Stub: produce deterministic plan with basic steps.
    steps=[]
    steps.append({"type":"fetch_payload","inputs":{"subject":subject}})
    steps.append({"type":"verify_signatures","inputs":{"subject":subject}})
    steps.append({"type":"apply_policy_precheck","inputs":{"target_platform":target_platform}})
    if target_platform in ("make","n8n"):
        steps.append({"type":"import_workflow","inputs":{"platform":target_platform}})
    elif target_platform == "wordpress":
        steps.append({"type":"install_plugin","inputs":{}})
    steps.append({"type":"configure_credentials","inputs":{"deps":deps}})
    steps.append({"type":"run_smoke_tests","inputs":{"default":True}})
    return {"subject":subject,"target_platform":target_platform,"mode":mode,"steps":steps}
