# ifos_dictionary_linter_stub_v1.py
from __future__ import annotations
from typing import List, Dict

def lint_terms(terms: List[Dict]) -> List[str]:
    errors=[]
    for t in terms:
        if not t.get("term_id","").startswith("term."):
            errors.append("term_id must start with term.")
    return errors
