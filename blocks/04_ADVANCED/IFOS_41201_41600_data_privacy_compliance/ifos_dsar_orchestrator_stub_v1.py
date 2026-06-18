# ifos_dsar_orchestrator_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def plan(dsar: Dict[str, Any]) -> Dict[str, Any]:
    t=dsar.get("type")
    if t=="access":
        return {"steps":["collect_sources","export_report","sign_evidence_pack"]}
    if t=="deletion":
        return {"steps":["locate_objects_via_lineage","apply_legal_hold_checks","delete_or_redact","generate_report","sign_evidence_pack"]}
    if t=="rectification":
        return {"steps":["locate_records","apply_updates","log_changes","generate_report"]}
    if t=="portability":
        return {"steps":["collect_sources","export_machine_readable","generate_report"]}
    return {"steps":["manual_review"]}
