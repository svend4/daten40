# IFOS Quality Assessor Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def assess(subject: Dict[str, Any]) -> Dict[str, Any]:
    gaps=[]
    level = subject.get("quality_level","L0")
    if level in {"L0","L1"} and not subject.get("contracts"):
        gaps.append("missing IOContract")
    if not subject.get("docs"):
        gaps.append("missing DocBundle")
    if not subject.get("tests"):
        gaps.append("missing TestSuite")
    target = "L3"
    return {"current_level":level,"target_level":target,"gaps":gaps,"recommendations":["add_contract","add_docs","add_tests"]}
