# IFOS SBOM Vulnerability Scan Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def scan(sbom: Dict[str, Any], vuln_db: Dict[str, Any]) -> Dict[str, Any]:
    findings=[]
    for c in sbom.get("components", []):
        name=c.get("name")
        ver=c.get("version")
        key=f"{name}:{ver}"
        for f in vuln_db.get(key, []):
            findings.append(f)
    return {"findings": findings}
