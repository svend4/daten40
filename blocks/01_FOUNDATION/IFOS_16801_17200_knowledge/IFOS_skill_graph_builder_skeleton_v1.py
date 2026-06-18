# IFOS Skill Graph Builder Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List, Tuple

def build_skill_graph(domain: str, assets: List[Dict[str, Any]]) -> Dict[str, Any]:
    # MVP heuristic: infer skills from asset tags.
    nodes = []
    edges = []
    seen = set()

    def add(skill_id, name, level, mapped):
        if skill_id in seen: return
        seen.add(skill_id)
        nodes.append({"skill_id":skill_id,"name":name,"level":level,"description":"","mapped_assets":mapped})

    # Simple mapping
    add("skill.install.bundle","Установить bundle одной кнопкой","L0",[a["id"] for a in assets if a.get("kind")=="bundle"])
    add("skill.secrets.vault","SecretRef и vault","L1",["secretref"])
    add("skill.monitoring.runs","Мониторинг runs","L2",["run_records"])
    add("skill.retries.backoff","Retry/backoff","L2",["rate_limits"])
    add("skill.cluster.vitrine","Кластеры и витрины","L3",["vitrine"])

    edges += [
        {"from":"skill.install.bundle","to":"skill.secrets.vault","type":"prereq"},
        {"from":"skill.secrets.vault","to":"skill.monitoring.runs","type":"enables"},
        {"from":"skill.monitoring.runs","to":"skill.retries.backoff","type":"enables"},
        {"from":"skill.retries.backoff","to":"skill.cluster.vitrine","type":"enables"}
    ]

    return {"graph_id":"sg.generated","subject_scope":{"domain":domain,"target":"any"},"nodes":nodes,"edges":edges,"version":"1.0.0","updated_at":""}
