# IFOS Quality Gates Stub v1
from __future__ import annotations
from typing import Dict, Any, List, Tuple

def run_quality_gates(record: Dict[str, Any]) -> Tuple[str, List[Dict[str, Any]]]:
    violations=[]
    title=record.get("canonical_title","")
    url=record.get("canonical_url","")
    text=record.get("content_text","")
    if not title:
        violations.append({"rule_id":"title_required","msg":"Title is empty","severity":"high"})
        return "rejected", violations
    if not (url.startswith("http://") or url.startswith("https://")):
        violations.append({"rule_id":"url_invalid","msg":"URL invalid","severity":"high"})
        return "quarantined", violations
    if len(text) < 80:
        violations.append({"rule_id":"text_short","msg":"Text too short","severity":"medium"})
        return "flagged", violations
    return "ok", violations
