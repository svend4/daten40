# IFOS Flow Executor Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def run_flow(flow: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Executes nodes in topological order (stub)."""
    # NOTE: No real DAG resolution here; just iterate nodes as listed.
    artifacts = {}
    for node in flow.get("nodes", []):
        ntype = node.get("type")
        if ntype == "ingest":
            artifacts["raw_items"] = [{"title":"demo","url":"https://example.com","published_at":"", "content":"..."}]
        elif ntype == "dedupe":
            artifacts["deduped_items"] = artifacts.get("raw_items", [])
        elif ntype == "rag_query":
            q = inputs.get("QUESTION","")
            artifacts["answer"] = f"DEMO ANSWER for: {q}"
            artifacts["sources"] = [{"title":"Example","url":"https://example.com"}]
        else:
            artifacts[f"{node.get('node_id','n')}_out"] = {}
    return {"status":"ok","artifacts":artifacts}
