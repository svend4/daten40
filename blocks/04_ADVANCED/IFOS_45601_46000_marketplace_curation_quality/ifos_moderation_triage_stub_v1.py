# ifos_moderation_triage_stub_v1.py
from __future__ import annotations
from typing import Dict

def triage(report: Dict) -> Dict:
    t=report.get("type","other")
    priority="high" if t in ("malware","review_fraud","plagiarism") else "medium"
    return {"case_id":"case.generated","state":"triage","priority":priority}
