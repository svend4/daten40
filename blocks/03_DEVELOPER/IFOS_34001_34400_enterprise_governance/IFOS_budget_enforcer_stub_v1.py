# IFOS Budget Enforcer Stub v1
from __future__ import annotations
from typing import Dict, Any, Tuple

def check_budget(rule: Dict[str, Any], usage: Dict[str, Any], cost_eur: float) -> Tuple[bool, str]:
    limit=float(rule.get("limits", {}).get("monthly_eur", 0))
    spent=float(usage.get("spent_monthly_eur", 0))
    if limit>0 and (spent + cost_eur) > limit:
        return False, "monthly budget exceeded"
    return True, "ok"
