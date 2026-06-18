# IFOS Form Builder Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List

def generate_form(title: str, requirements: List[Dict[str, Any]]) -> Dict[str, Any]:
    fields = []
    for r in requirements or []:
        fields.append({"id":r["name"].lower().replace(" ","_"),"label":r["name"],"type":"text","required":bool(r.get("required",True)),"help":r.get("help",""),"secret":r.get("type")=="secret"})
    return {"form_id":"form.generated","title":title,"fields":fields,"validation":{"schema_ref":"","rules":[]},"storage":{"secret_store":"vault","redaction":True,"ttl_days":0},"version":"1.0.0","updated_at":""}
