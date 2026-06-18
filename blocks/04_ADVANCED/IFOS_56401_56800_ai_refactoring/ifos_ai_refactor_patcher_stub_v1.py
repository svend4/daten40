# ifos_ai_refactor_patcher_stub_v1.py
from __future__ import annotations
from typing import Dict

def make_patch(plan: Dict) -> Dict:
    # Placeholder patch generator
    return {
        "patch_id": "ptc.generated",
        "target_ref": plan.get("target_ref",""),
        "diff": "\n".join(plan.get("changes",[])),
        "applies_to_version": "unknown",
        "rollback": "restore snapshot",
        "version": "1.0.0",
    }
