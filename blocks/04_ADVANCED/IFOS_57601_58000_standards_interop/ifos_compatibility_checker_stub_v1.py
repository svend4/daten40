# ifos_compatibility_checker_stub_v1.py
from __future__ import annotations
from typing import List, Dict

def build_matrix(runtime_ref: str, conformance_results: List[Dict]) -> Dict:
    rows=[]
    for r in conformance_results:
        rows.append({"connector": r.get("connector_ref"), "status": "supported" if r.get("status")=="PASS" else "warn"})
    return {"matrix_id":"mtx.generated","runtime_ref":runtime_ref,"rows":rows,"version":"1.0.0"}
