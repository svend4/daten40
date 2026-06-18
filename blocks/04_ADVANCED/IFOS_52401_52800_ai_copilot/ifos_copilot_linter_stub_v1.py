# ifos_copilot_linter_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def lint(plan: Dict) -> List[Dict]:
    findings=[]
    bundles=plan.get("bundles",[])
    if "bun.output" in bundles and "bun.rollback" not in bundles:
        findings.append({"severity":"warn","message":"Output bundle has no rollback","autofix":{"add":"bun.rollback"}})
    return findings
