# ifos_scheduler_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List

def pick(queue_state: Dict[str, Any], jobs: List[Dict[str, Any]], priority_policy: Dict[str, Any]) -> Dict[str, Any] | None:
    # Stub: choose first queued job (real: weights + fairness + aging)
    for j in jobs:
        if j.get("status") == "queued":
            return j
    return None
