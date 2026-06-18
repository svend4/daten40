# ifos_explainer_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def explain(plan: Dict[str,Any]) -> Dict[str,Any]:
    return {"why":["Chosen level="+plan.get("level","")], "risks":["rate limits"], "actions":["set backoff"]}
