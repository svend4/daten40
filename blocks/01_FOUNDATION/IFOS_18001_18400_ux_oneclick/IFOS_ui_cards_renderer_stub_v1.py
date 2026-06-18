# IFOS UI Cards Renderer Stub v1
from __future__ import annotations
from typing import Dict, Any
import json

def render_card(card: Dict[str, Any]) -> str:
    # Returns a simple HTML snippet (stub)
    title = card.get("title","")
    summary = card.get("summary","")
    bullets = "".join(f"<li>{b}</li>" for b in (card.get("bullets") or []))
    badges = " ".join(f"<span class='badge'>{x}</span>" for x in (card.get("badges") or []))
    return f"<h2>{title}</h2><p>{summary}</p><div>{badges}</div><ul>{bullets}</ul>"
