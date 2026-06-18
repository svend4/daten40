# IFOS Workflow Explainer Stub v1
from __future__ import annotations
from typing import Dict, Any

def explain_workflow(platform: str, workflow: Dict[str, Any]) -> Dict[str, Any]:
    # Stub: real version parses Make/n8n/WP/native configs
    return {
        "explain_id":"exp.generated",
        "workflow_ref":workflow.get("ref",""),
        "platform":platform,
        "summary":"Auto explanation (stub)",
        "blocks":[],
        "dataflow":[],
        "risks":[],
        "improvements":[],
        "refs":[],
        "version":"1.0.0",
        "updated_at":""
    }
