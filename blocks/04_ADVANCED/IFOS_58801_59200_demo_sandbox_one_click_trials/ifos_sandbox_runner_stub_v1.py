# ifos_sandbox_runner_stub_v1.py
from __future__ import annotations
from typing import Dict

def run_trial(trial_bundle: Dict) -> Dict:
    # Placeholder: simulate success
    return {"trial_id": trial_bundle.get("trial_id"), "status": "OK", "outputs": {"vitrine_url": "sandbox://vitrines/demo/123"}}
