# ifos_locale_negotiation_stub_v1.py
from __future__ import annotations
from typing import List

def negotiate(accept_language: str, supported: List[str]) -> str:
    # Very small stub: pick first supported that appears in header
    langs=[p.split(";")[0].strip() for p in accept_language.split(",")]
    for l in langs:
        if l in supported:
            return l
        # language-only fallback
        base=l.split("-")[0]
        for s in supported:
            if s.startswith(base+"-") or s==base:
                return s
    return supported[0] if supported else "en"
