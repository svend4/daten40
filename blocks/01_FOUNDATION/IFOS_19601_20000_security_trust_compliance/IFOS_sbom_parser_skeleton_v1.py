# IFOS SBOM Parser Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List

def parse_sbom(sbom_obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Normalize to list of components with name/version/purl/hash/license
    return sbom_obj.get("components", [])

def find_license_issues(licenses: List[str], denylist: List[str]) -> List[str]:
    return [lic for lic in licenses if lic in denylist]
