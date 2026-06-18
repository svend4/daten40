# ifos_docs_linter_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def lint(doc_bundle: Dict) -> List[str]:
    errors=[]
    if not doc_bundle.get("passport"):
        errors.append("missing_passport")
    if not doc_bundle.get("quickstart"):
        errors.append("missing_quickstart")
    return errors
