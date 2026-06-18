# IFOS Explainer Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def explain(candidate_id: str, intents: List[str], constraints: Dict[str, Any]) -> Dict[str, Any]:
    reasons=[f"Поддерживает intents: {', '.join(intents)}"]
    if constraints.get("gdpr"): reasons.append("Совместимо с режимом GDPR (ограничение логов/PII)")
    if constraints.get("no_code"): reasons.append("Есть готовая кнопка установки (bundle)")
    return {"decision":"recommend","reasons":reasons,"confidence":0.7}
