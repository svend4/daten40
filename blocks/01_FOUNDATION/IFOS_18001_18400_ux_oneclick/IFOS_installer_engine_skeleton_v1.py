# IFOS Installer Engine Skeleton v1
from __future__ import annotations
from typing import Dict, Any, Tuple

def create_wizard(subject: Dict[str, Any], mode: str) -> Dict[str, Any]:
    return {"wizard_id":"wiz.generated","subject":subject,"mode":mode,"steps":[],"install_plan_ref":"plan.generated","version":"1.0.0","updated_at":""}

def complete_step(wizard: Dict[str, Any], step_id: str, inputs: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    # returns updated wizard + telemetry/audit payloads (stub)
    return wizard, {"event":"wizard_step_complete","step_id":step_id}
