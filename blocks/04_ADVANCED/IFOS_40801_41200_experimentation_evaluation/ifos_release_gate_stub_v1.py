# ifos_release_gate_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

OPS = {
    "<": lambda x,y: x<y,
    "<=": lambda x,y: x<=y,
    "==": lambda x,y: x==y,
    ">=": lambda x,y: x>=y,
    ">": lambda x,y: x>y,
}

def evaluate(metrics: Dict[str, float], gate: Dict[str, Any]) -> str:
    for c in gate.get("conditions", []):
        m=c["metric"]; op=c["op"]; v=float(c["value"])
        if m not in metrics:
            return "require_approval"
        if not OPS[op](float(metrics[m]), v):
            return "block"
    return "allow"
