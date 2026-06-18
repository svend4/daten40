# IFOS Policy Engine Skeleton v1
from __future__ import annotations
from typing import Dict, Any, Tuple

def evaluate_gate(asset: Dict[str, Any], policy_profile: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    # asset: contains flags like sbom_present, signature_valid, evidence_level, licenses_known, webhooks_used, network_used
    mode = policy_profile.get("mode","personal")
    reasons = []
    decision = "allow"

    for rule in policy_profile.get("rules", []) or []:
        rtype = rule.get("type")
        rdec = rule.get("decision")
        cond = rule.get("conditions", {}) or {}

        if rtype == "sbom" and cond.get("require") and not asset.get("sbom_present"):
            decision = "deny" if rdec == "deny" else "allow_with_conditions"
            reasons.append("SBOM missing")

        if rtype == "signature" and cond.get("require_valid_signature") and not asset.get("signature_valid"):
            decision = "deny" if mode in ("b2b","government") else "allow_with_conditions"
            reasons.append("Signature missing/invalid")

        if rtype == "license" and cond.get("require_known_licenses") and not asset.get("licenses_known"):
            decision = "deny" if mode == "government" else "allow_with_conditions"
            reasons.append("Unknown licenses")

        if rtype == "webhooks" and rule.get("decision") == "deny" and asset.get("webhooks_used"):
            decision = "deny"
            reasons.append("Webhooks forbidden in this mode")

        if rtype == "network" and asset.get("network_used"):
            req = cond.get("require_evidence_level")
            if req and (asset.get("evidence_level","L0") < req):
                decision = "deny" if mode == "government" else "allow_with_conditions"
                reasons.append(f"Network requires evidence >= {req}")

    return decision, {"mode":mode, "reasons":reasons}
