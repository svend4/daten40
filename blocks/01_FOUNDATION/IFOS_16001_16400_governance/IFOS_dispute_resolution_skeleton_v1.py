# IFOS Dispute Resolution Skeleton v1
# A simple state machine for dispute cases.
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import datetime

ALLOWED_TRANSITIONS = {
    "open": ["investigating", "closed"],
    "investigating": ["resolved", "closed"],
    "resolved": ["appealed", "closed"],
    "appealed": ["resolved", "closed"],
    "closed": []
}

@dataclass
class DisputeCase:
    case_id: str
    status: str = "open"
    timeline: List[Dict[str, Any]] = field(default_factory=list)
    decision: Dict[str, Any] = field(default_factory=dict)
    appeal_ref: str = ""

    def log(self, event: str, actor: str):
        ts = datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"
        self.timeline.append({"ts": ts, "event": event, "actor": actor})

    def transition(self, new_status: str, actor: str):
        if new_status not in ALLOWED_TRANSITIONS.get(self.status, []):
            raise ValueError(f"Illegal transition: {self.status} -> {new_status}")
        self.log(f"Status changed {self.status} -> {new_status}", actor)
        self.status = new_status

    def set_decision(self, verdict: str, reasoning: str, sanctions: List[str], actor: str):
        self.decision = {"verdict": verdict, "reasoning": reasoning, "sanctions": sanctions,
                         "effective_from": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"}
        self.log(f"Decision set: {verdict}", actor)

def auto_triage(case: DisputeCase, antifraud_max_score: float, malware_found: bool) -> Optional[str]:
    # returns suggested sanction type
    if malware_found:
        return "delist"
    if antifraud_max_score >= 85:
        return "freeze_score"
    if antifraud_max_score >= 70:
        return "quarantine"
    return None

if __name__ == "__main__":
    c = DisputeCase("case.demo.001")
    c.log("Case filed", "usr.reporter01")
    c.transition("investigating", "mod.mary")
    suggested = auto_triage(c, antifraud_max_score=88, malware_found=False)
    if suggested:
        c.log(f"Auto-triage suggests sanction: {suggested}", "system")
    c.set_decision("partial", "Remove suspicious reviews and freeze score for 30 days.", [suggested or ""], "panel.v1")
    c.transition("resolved", "panel.v1")
    print(c.status, c.decision)
