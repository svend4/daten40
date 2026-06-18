# IFOS Alert Evaluator Stub v1
from __future__ import annotations
from typing import Dict, Any

OPS={">":lambda a,b:a>b,"<":lambda a,b:a<b,">=":lambda a,b:a>=b,"<=":lambda a,b:a<=b,"==":lambda a,b:a==b,"!=":lambda a,b:a!=b}

def evaluate(rule: Dict[str, Any], metrics: Dict[str, float]) -> bool:
    cond=rule["condition"]
    m=metrics.get(cond["metric"])
    if m is None:
        return False
    return OPS[cond["op"]](m, float(cond["threshold"]))
