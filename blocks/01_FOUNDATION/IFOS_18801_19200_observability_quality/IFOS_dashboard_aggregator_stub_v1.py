# IFOS Dashboard Aggregator Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def summarize(subject: Dict[str, Any], period: str, kpis: List[Dict[str, Any]], alerts: List[Dict[str, Any]]) -> Dict[str, Any]:
    headline = "OK" if not any(a.get("level") == "critical" for a in alerts) else "Needs attention"
    return {
        "dashboard_id": "dash.generated",
        "subject": subject,
        "period": period,
        "headline": headline,
        "kpis": kpis,
        "alerts": alerts,
        "version": "1.0.0",
        "updated_at": ""
    }
