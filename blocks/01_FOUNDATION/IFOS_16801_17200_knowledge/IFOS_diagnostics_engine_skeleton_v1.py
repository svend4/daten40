# IFOS Diagnostics Engine Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List

def analyze_run(run: Dict[str, Any], known_issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    status = run.get("status","fail")
    logs = run.get("logs","")
    signals = []
    hypotheses = []
    quick = []
    deep = []
    links = []

    if "401" in logs or run.get("error",{}).get("code") == "401":
        signals.append({"name":"http_status","value":"401","severity":"high"})
        hypotheses.append({"cause":"Неверный/отозванный токен","prob":0.8,"evidence":["401 in logs"]})
        quick.append("Обновите токен в vault/SecretRef и повторите smoke test.")
        links.append("tut.telegram.token.setup")

    if "429" in logs:
        signals.append({"name":"http_status","value":"429","severity":"medium"})
        hypotheses.append({"cause":"Rate limit","prob":0.6,"evidence":["429 in logs"]})
        quick.append("Включите retry/backoff и батчинг.")
        links.append("tut.telegram.ratelimit")

    # Fallback
    if not hypotheses:
        hypotheses.append({"cause":"Несовпадение полей/версий или sandbox запрет","prob":0.5,"evidence":["no specific signature"]})
        deep.append("Сравните contract expectations и реальные данные; проверьте policy decisions.")

    return {
        "report_id":"diag.generated",
        "run_id":run.get("run_id",""),
        "status":status,
        "signals":signals,
        "hypotheses":hypotheses,
        "quick_fixes":quick[:3],
        "deep_fixes":deep[:3],
        "links":links[:5],
        "generated_at":"",
        "method_version":"diag.v1"
    }
