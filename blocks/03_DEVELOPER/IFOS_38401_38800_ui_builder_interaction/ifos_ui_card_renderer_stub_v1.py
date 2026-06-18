# ifos_ui_card_renderer_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def render_card(card: Dict[str, Any]) -> str:
    title=card.get("title","")
    desc=card.get("description","")
    risk=card.get("risk","safe")
    return f"<div class='card risk-{risk}'><h3>{title}</h3><p>{desc}</p></div>"
