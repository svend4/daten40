# IFOS Incident Workflow Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def actions_for_incident(incident: Dict[str, Any]) -> List[Dict[str, Any]]:
    t=incident.get("type")
    acts=[]
    if t in ("malware","phishing"):
        acts.append({"kind":"disable_bundle"})
        acts.append({"kind":"revoke_keys"})
        acts.append({"kind":"notify_users"})
    if t in ("vuln_exploit","policy_breach","data_leak"):
        acts.append({"kind":"block_version"})
        acts.append({"kind":"notify_admins"})
        acts.append({"kind":"generate_report"})
    return acts
