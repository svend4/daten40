# ifos_compare_report_generator_stub_v1.py
from __future__ import annotations
from typing import List, Dict

def generate(runs: List[Dict]) -> Dict:
    # Very simple: choose best overall
    best=max(runs, key=lambda r: r.get("overall",0))
    return {"winner": best.get("artifact_ref"), "runs": runs}
