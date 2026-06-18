# ifos_explainability_bundle_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List

def build(run_id: str, citations: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"run_id": run_id, "citations": citations, "policies": [], "decisions": [], "risks": []}
