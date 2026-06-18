# IFOS Synonym Expander Stub v1
from __future__ import annotations
from typing import Dict, List

def expand(query: str, synonym_map: Dict[str, List[str]]) -> List[str]:
    # very simple: if token appears, add synonyms
    terms=set([query])
    for norm, vars in synonym_map.items():
        for v in vars:
            if v.lower() in query.lower():
                for add in vars:
                    terms.add(query.lower().replace(v.lower(), add.lower()))
    return list(terms)
