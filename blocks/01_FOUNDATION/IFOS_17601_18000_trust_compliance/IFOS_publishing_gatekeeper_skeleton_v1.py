# IFOS Publishing Gatekeeper Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List

def can_one_click_install(asset_state: Dict[str, Any]) -> bool:
    return asset_state.get("gate_decision") in ("allow","allow_with_conditions") and asset_state.get("docs_complete", False)

def can_list_in_marketplace(asset_state: Dict[str, Any]) -> bool:
    return asset_state.get("gate_decision") == "allow" and asset_state.get("fraud_clean", True)

def can_be_featured(asset_state: Dict[str, Any]) -> bool:
    return (asset_state.get("gate_decision") == "allow"
            and asset_state.get("evidence_level","L0") >= "L2"
            and asset_state.get("rating_evidence_weighted",0) >= 4.2
            and asset_state.get("sbom_present", False)
            and asset_state.get("signature_valid", False))
