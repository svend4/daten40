# IFOS Autodiagnostics Engine Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def diagnose(symptom: str, evidence: Dict[str, Any]) -> Dict[str, Any]:
    # Very simplified rule-based diagnostics.
    causes = []
    if "E_SECRET_MISSING" in (evidence.get("codes") or []):
        causes.append({"cause":"Missing secret_ref","code":"E_SECRET_MISSING","fix_hint":"Create secret_ref and fill value"})
    if "timeout" in symptom.lower():
        causes.append({"cause":"Network timeout","code":"E_CONN_TIMEOUT","fix_hint":"Check connector health/quota"})
    conf = 0.8 if causes else 0.3
    return {"symptom": symptom, "probable_causes": causes, "confidence": conf}
