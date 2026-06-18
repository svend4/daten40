# ifos_pluralization_stub_v1.py
from __future__ import annotations

def plural_ru(n: int, one: str, few: str, many: str) -> str:
    n=abs(n)
    if n%10==1 and n%100!=11: return one
    if 2<=n%10<=4 and not (12<=n%100<=14): return few
    return many
