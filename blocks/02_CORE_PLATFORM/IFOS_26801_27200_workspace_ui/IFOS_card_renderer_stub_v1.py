# IFOS Card Renderer Stub v1
from __future__ import annotations
from typing import Dict, Any

def render(card: Dict[str, Any], layout: Dict[str, Any]) -> Dict[str, Any]:
    """Return a UI description object for frontend (stub)."""
    return {
        "title": card.get("title"),
        "tabs": sorted(set([s.get("tab","Main") for s in layout.get("sections", [])])),
        "sections": layout.get("sections", []),
        "actions": card.get("actions", []),
        "status": card.get("status")
    }
