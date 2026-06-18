# IFOS Moderation Pipeline Stub v1
from __future__ import annotations
from typing import Dict, Any

def spam_score(review: Dict[str, Any]) -> float:
    text = review.get("text","")
    if len(text) < 10: return 0.6
    if "http://" in text or "https://" in text: return 0.3
    return 0.1

def decide_action(abuse_report: Dict[str, Any]) -> Dict[str, Any]:
    cat = abuse_report.get("category")
    if cat in {"phishing","malware"}:
        return {"action":"quarantine_subject","reason":"high risk report"}
    return {"action":"require_verification","reason":"needs triage"}
