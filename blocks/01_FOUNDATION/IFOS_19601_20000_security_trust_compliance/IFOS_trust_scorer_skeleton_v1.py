# IFOS Trust Scorer Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List

DEFAULT_WEIGHTS = {
    "SignatureVerified": 0.25,
    "SBOMComplete": 0.15,
    "VulnerabilityRisk": 0.25,
    "PolicyCompliance": 0.15,
    "PermissionsRisk": 0.10,
    "IncidentHistory": 0.10,
}

def clamp(x: float) -> float:
    return max(0.0, min(1.0, x))

def compute(components: List[Dict[str, Any]]) -> float:
    total = 0.0
    for c in components:
        total += float(c["value"]) * float(c["weight"])
    return clamp(total)

def trust_score_from_context(ctx: Dict[str, Any]) -> Dict[str, Any]:
    # ctx should be prepared by pipeline: signature_verified, sbom_complete_ratio, vuln_risk, policy_score, perms_risk, incident_risk
    comps = [
        {"name":"SignatureVerified","value":1.0 if ctx.get("signature_verified") else 0.0,"weight":DEFAULT_WEIGHTS["SignatureVerified"],"notes":""},
        {"name":"SBOMComplete","value":float(ctx.get("sbom_complete_ratio", 0.0)),"weight":DEFAULT_WEIGHTS["SBOMComplete"],"notes":""},
        {"name":"VulnerabilityRisk","value":float(ctx.get("vuln_risk", 1.0)),"weight":DEFAULT_WEIGHTS["VulnerabilityRisk"],"notes":""},
        {"name":"PolicyCompliance","value":float(ctx.get("policy_score", 1.0)),"weight":DEFAULT_WEIGHTS["PolicyCompliance"],"notes":""},
        {"name":"PermissionsRisk","value":float(ctx.get("perms_risk", 1.0)),"weight":DEFAULT_WEIGHTS["PermissionsRisk"],"notes":""},
        {"name":"IncidentHistory","value":float(ctx.get("incident_risk", 1.0)),"weight":DEFAULT_WEIGHTS["IncidentHistory"],"notes":""},
    ]
    return {"score": compute(comps), "components": comps}
