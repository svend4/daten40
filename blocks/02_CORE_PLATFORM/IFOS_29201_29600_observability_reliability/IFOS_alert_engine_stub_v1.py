# IFOS Alert Engine Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def evaluate_rule(rule: Dict[str, Any], metric_value: float) -> bool:
    op = rule["condition"]["op"]
    val = float(rule["condition"]["value"])
    if op == ">": return metric_value > val
    if op == "<": return metric_value < val
    if op == ">=": return metric_value >= val
    if op == "<=": return metric_value <= val
    if op == "==": return metric_value == val
    return False

def evaluate(rules: List[Dict[str, Any]], metrics: Dict[str, float]) -> List[Dict[str, Any]]:
    fired = []
    for r in rules:
        if not r.get("enabled", True):
            continue
        metric = r["condition"]["metric"]
        v = float(metrics.get(metric, 0.0))
        if evaluate_rule(r, v):
            fired.append({"rule_id": r["rule_id"], "severity": r["severity"], "metric": metric, "value": v})
    return fired
