# ifos_learning_auto_grader_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def grade(lab_run: Dict) -> Dict:
    # Placeholder: check presence of required artifacts/events
    required = lab_run.get("grading",{}).get("must_create",[])
    created = set(lab_run.get("created",[]))
    ok = all(r in created for r in required)
    return {"passed": ok, "score": 10 if ok else 5}
