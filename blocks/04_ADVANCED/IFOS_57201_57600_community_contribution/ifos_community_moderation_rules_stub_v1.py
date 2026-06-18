# ifos_community_moderation_rules_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def evaluate(target: Dict, reports: List[Dict]) -> Dict:
    # Placeholder: quarantine if many reports
    if len(reports) >= 5:
        return {"action":"quarantine","reason_code":"multiple_reports"}
    return {"action":"allow"}
