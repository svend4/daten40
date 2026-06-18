# ifos_support_macro_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def render(template: str, ctx: Dict[str, Any]) -> str:
    out=template
    for k,v in ctx.items():
        out=out.replace("{"+k+"}", str(v))
    return out
