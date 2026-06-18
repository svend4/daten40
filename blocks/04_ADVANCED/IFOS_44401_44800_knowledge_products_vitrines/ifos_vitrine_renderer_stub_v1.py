# ifos_vitrine_renderer_stub_v1.py
from __future__ import annotations
from typing import List, Dict

def render(vitrine: Dict, cards: List[Dict]) -> str:
    # stub: returns a minimal markdown page
    lines=[f"# {vitrine['title']}"]
    if vitrine.get("description"): lines.append(vitrine["description"])
    lines.append("")
    for c in cards:
        lines.append(f"## {c['title']}")
        lines.append(c["what_it_does"])
        lines.append("")
    return "\n".join(lines)
