# IFOS Dataset Manager Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def create_version(dataset_id: str, prev_version: str, changes: Dict[str, Any]) -> Dict[str, Any]:
    # changes could include added/updated/removed counts and refs
    return {
        "dataset_id": dataset_id,
        "version_id": changes.get("version_id"),
        "diff_summary": changes.get("diff_summary",""),
        "snapshot_refs": changes.get("snapshot_refs", []),
        "migration": {"from": prev_version, "steps": changes.get("migration_steps", [])},
    }
