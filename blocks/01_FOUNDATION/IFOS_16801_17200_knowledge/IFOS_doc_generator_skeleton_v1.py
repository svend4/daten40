# IFOS Doc Generator Skeleton v1
# Builds Doc Cards from contracts + install plans + run history.
from __future__ import annotations
from typing import Dict, Any, List

def generate_doc_card(subject: Dict[str, Any],
                      contract: Dict[str, Any],
                      install_plan: Dict[str, Any],
                      run_stats: Dict[str, Any],
                      common_failures: List[Dict[str, Any]]) -> Dict[str, Any]:
    title = subject.get("id","").replace("_"," ")
    summary = contract.get("summary","Generated from contract + runs.")
    inputs = [{"name":k,"type":"string","required":True,"description":v} for k,v in (contract.get("inputs",{}) or {}).items()]
    outputs = [{"name":k,"type":"string","description":v} for k,v in (contract.get("outputs",{}) or {}).items()]

    examples = contract.get("examples", []) or []
    errors = []
    for f in common_failures or []:
        errors.append({
            "symptom": f.get("symptom",""),
            "likely_cause": f.get("cause",""),
            "fix": f.get("fix",""),
            "link_tutorial": f.get("tutorial","")
        })

    evidence = {"level": run_stats.get("evidence_level","L0"), "refs": run_stats.get("evidence_refs",[])}
    return {
        "doc_id": "doc.generated",
        "subject": subject,
        "title": title,
        "summary": summary,
        "io": {"inputs": inputs, "outputs": outputs},
        "examples": examples,
        "common_errors": errors,
        "evidence": evidence,
        "updated_at": run_stats.get("updated_at",""),
        "version": "1.0.0"
    }
