# IFOS Doc Generator from Schema Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List
import json

def table_from_jsonschema(schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Simplified: extracts top-level properties
    props = schema.get("properties", {}) or {}
    rows = []
    for k,v in props.items():
        rows.append({
            "field": k,
            "type": v.get("type",""),
            "required": k in (schema.get("required",[]) or []),
            "description": v.get("description","")
        })
    return rows

def generate_doc_page(subject: Dict[str, Any], schema_in: Dict[str, Any], schema_out: Dict[str, Any]) -> Dict[str, Any]:
    in_rows = table_from_jsonschema(schema_in)
    out_rows = table_from_jsonschema(schema_out)
    body_io = "Inputs:\\n" + "\\n".join([f"- {r['field']} ({r['type']})" for r in in_rows]) + "\\n\\nOutputs:\\n" + "\\n".join([f"- {r['field']} ({r['type']})" for r in out_rows])
    return {
        "page_id":"page.generated",
        "subject":subject,
        "title":f"{subject.get('id','asset')} — docs",
        "sections":[
            {"id":"overview","title":"Overview","body":"Auto-generated overview (stub).","refs":[]},
            {"id":"io","title":"Inputs/Outputs","body":body_io,"refs":[]},
        ],
        "render":{"format":"md","content_ref":""},
        "version":"1.0.0",
        "updated_at":""
    }
