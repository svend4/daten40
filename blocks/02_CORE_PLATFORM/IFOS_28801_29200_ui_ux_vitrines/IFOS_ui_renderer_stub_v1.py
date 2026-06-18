# IFOS UI Renderer Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def render_card(card: Dict[str, Any]) -> str:
    # Simplified HTML rendering
    title = card.get("title","")
    summary = card.get("summary","")
    status = card.get("status","unknown")
    actions = card.get("actions",[]) or []
    btns = "".join([f"<button>{a.get('label','Action')}</button>" for a in actions])
    return f"<div class='card'><h3>{title}</h3><p>{summary}</p><span>{status}</span>{btns}</div>"

def render_vitrine(vitrine: Dict[str, Any], cards: List[Dict[str, Any]]) -> str:
    body = "".join(render_card(c) for c in cards)
    return f"<section><h2>{vitrine.get('title','')}</h2><p>{vitrine.get('goal','')}</p>{body}</section>"
