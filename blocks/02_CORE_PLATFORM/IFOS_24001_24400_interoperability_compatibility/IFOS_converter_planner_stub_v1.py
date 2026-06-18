# IFOS Converter Planner Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def plan_conversion(source_ir: Dict[str, Any], target_platform: str, adapter_index: Dict[str, str]) -> Dict[str, Any]:
    # source_ir: nodes with contract_id; adapter_index maps (contract_id,target_platform)->adapter_id
    steps=[]
    manual=[]
    for node in source_ir.get("nodes", []):
        key=f"{node.get('contract_id')}::{target_platform}"
        adapter_id = adapter_index.get(key)
        if not adapter_id:
            steps.append({"node": node.get("id"), "adapter_id": None, "status":"needs_manual", "notes":"adapter missing"})
            manual.append(node.get("id"))
        else:
            steps.append({"node": node.get("id"), "adapter_id": adapter_id, "status":"planned"})
    return {"plan_id":"cp.demo","source_platform":source_ir.get("platform"),"target_platform":target_platform,"steps":steps,"manual_flags":manual}
