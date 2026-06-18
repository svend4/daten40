# IFOS Synonym Expander Stub v1
from __future__ import annotations
from typing import Dict, List, Set

def expand(query_tokens: List[str], synsets: Dict[str, List[str]], mode: str = "expansive") -> List[str]:
    # synsets: canonical -> members
    if mode == "strict":
        return query_tokens
    expanded: List[str] = []
    for tok in query_tokens:
        expanded.append(tok)
        # if token matches canonical, expand; if token is a member, also expand to canonical
        for canon, members in synsets.items():
            if tok == canon or tok in members:
                expanded.extend(members)
                expanded.append(canon)
    # dedupe
    seen: Set[str] = set()
    res=[]
    for t in expanded:
        if t not in seen:
            seen.add(t); res.append(t)
    return res
