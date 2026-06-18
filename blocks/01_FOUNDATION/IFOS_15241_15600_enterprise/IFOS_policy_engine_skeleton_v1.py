# IFOS Policy Engine Skeleton v1
# Evaluates RBAC/ABAC rules and returns ALLOW / DENY / ALLOW_WITH_CONDITIONS.

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Tuple

@dataclass
class Decision:
    effect: str  # ALLOW / DENY / ALLOW_WITH_CONDITIONS
    reason: str
    conditions: Dict[str, Any]

def match_action(rule: Dict[str, Any], action: str) -> bool:
    return action in (rule.get("actions") or [])

def match_role(rule: Dict[str, Any], roles: List[str]) -> bool:
    allowed = set(rule.get("roles") or [])
    return bool(allowed.intersection(set(roles)))

def match_resource_type(rule: Dict[str, Any], resource_type: str) -> bool:
    rts = rule.get("resource_types")
    return True if not rts else resource_type in rts

def eval_conditions(conds: Dict[str, Any], ctx: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], str]:
    # MVP: minimal condition checks: min_level, require_2fa, flags match
    if not conds:
        return True, {}, "no conditions"

    required = {}
    # require_2fa: if ctx says satisfied, ok else return conditions
    if "require_2fa" in conds:
        required["require_2fa"] = True
        if not ctx.get("2fa_ok", False):
            return False, required, "2FA required"

    if "min_level" in conds:
        required["min_level"] = conds["min_level"]
        # ctx must provide evidence_level in comparable ordering
        order = {"L0_schema":0,"L1_dry_run":1,"L2_integration":2,"L3_production":3}
        if order.get(ctx.get("evidence_level","L0_schema"),0) < order.get(conds["min_level"],0):
            return False, required, "Evidence level too low"

    if "flags" in conds:
        required["flags"] = conds["flags"]
        flags = ctx.get("flags") or {}
        for k,v in conds["flags"].items():
            if flags.get(k) != v:
                return False, required, f"Flag mismatch for {k}"

    return True, required, "conditions satisfied"

def decide(policy: Dict[str, Any], subject_roles: List[str], action: str, resource_type: str, ctx: Dict[str, Any]) -> Decision:
    rules = policy.get("rules") or []
    # DENY rules should win if matched
    deny_hits = []
    allow_hits = []
    allow_cond_hits = []

    for r in rules:
        if not match_action(r, action): 
            continue
        if not match_role(r, subject_roles):
            continue
        if not match_resource_type(r, resource_type):
            continue

        effect = r.get("effect")
        conds = r.get("conditions") or {}
        ok, required, note = eval_conditions(conds, ctx)

        if effect == "DENY":
            deny_hits.append((r.get("rule_id",""), note))
        elif effect == "ALLOW":
            allow_hits.append((r.get("rule_id",""), note))
        elif effect == "ALLOW_WITH_CONDITIONS":
            if ok:
                allow_hits.append((r.get("rule_id",""), note))
            else:
                allow_cond_hits.append((r.get("rule_id",""), required, note))

    if deny_hits:
        rid, note = deny_hits[0]
        return Decision("DENY", f"Denied by {rid}: {note}", {})

    if allow_hits:
        rid, note = allow_hits[0]
        return Decision("ALLOW", f"Allowed by {rid}: {note}", {})

    if allow_cond_hits:
        rid, required, note = allow_cond_hits[0]
        return Decision("ALLOW_WITH_CONDITIONS", f"Needs conditions from {rid}: {note}", required)

    return Decision("DENY", "No matching rule", {})

if __name__ == "__main__":
    sample_policy = {
      "rules":[
        {"rule_id":"r1","effect":"ALLOW","actions":["run_job"],"roles":["Operator"],"resource_types":["job"]},
        {"rule_id":"r2","effect":"ALLOW_WITH_CONDITIONS","actions":["publish_evidence"],"roles":["Verifier"],"resource_types":["evidence_record"],
         "conditions":{"require_2fa":True,"min_level":"L2_integration"}}
      ]
    }
    print(decide(sample_policy, ["Verifier"], "publish_evidence", "evidence_record", {"2fa_ok":False,"evidence_level":"L1_dry_run"}))
