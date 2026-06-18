# IFOS Macro Compiler Stub v1
from __future__ import annotations
from typing import Dict, Any

def apply_macro(flow: Dict[str, Any], macro: Dict[str, Any], insert_after_node_id: str) -> Dict[str, Any]:
    """Insert macro snippet nodes/edges after a given node (stub)."""
    snippet = macro.get("snippet_flow", {})
    new_flow = dict(flow)
    new_flow["nodes"] = list(flow.get("nodes", [])) + list(snippet.get("nodes", []))
    new_flow["edges"] = list(flow.get("edges", [])) + list(snippet.get("edges", []))
    return new_flow
