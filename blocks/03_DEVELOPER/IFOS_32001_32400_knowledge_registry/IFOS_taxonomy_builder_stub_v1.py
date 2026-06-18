# IFOS Taxonomy Builder Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def classify_item_by_keywords(text: str) -> List[str]:
    # Very naive classifier. Replace with embedding classifier later.
    paths=[]
    t=text.lower()
    if "pdf" in t:
        paths.append("Docs/Parse/PDF")
    if "wordpress" in t or "wp" in t:
        paths.append("CMS/WordPress/Plugins")
    if "telegram" in t:
        paths.append("Messaging/Telegram")
    return paths
