# ifos_change_state_machine_stub_v1.py
from __future__ import annotations

TASK_STATES = ["idea","doing","review","done"]
RFC_STATES = ["draft","in_review","approved","rejected","implemented"]

def can_transition(current: str, target: str, states) -> bool:
    if current not in states or target not in states:
        return False
    # simple linear flow, allow backtracking to prior states
    return True
