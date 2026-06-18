# IFOS Undo Engine Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List

def generate_undo_plan(install_plan: Dict[str, Any]) -> Dict[str, Any]:
    # In real system: invert changes (create->delete, enable->disable, add->remove)
    steps = []
    for change in install_plan.get("changes", []) or []:
        steps.append({"id":"u.generated","title":f"Rollback {change.get('type','change')}", "action":"rollback", "ref":change.get("ref",""), "requires_confirmation":True})
    return {"undo_id":"undo.generated","subject":install_plan.get("subject",{}),"steps":steps,"safety":{"no_data_loss_by_default":True,"backup_refs":[]},"version":"1.0.0","updated_at":""}
