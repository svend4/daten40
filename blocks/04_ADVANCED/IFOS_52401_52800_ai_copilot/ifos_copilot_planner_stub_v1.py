# ifos_copilot_planner_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

LEVELS={
  "simple":["bun.ingest","bun.transform","bun.output"],
  "medium":["bun.ingest","bun.dedup","bun.ai_summary","bun.approval","bun.output"],
  "enterprise":["bun.ingest","bun.dedup","bun.data_os","bun.ops_os","bun.approval","bun.output"]
}

def generate_plan(intent: Dict[str,Any], level: str="medium") -> Dict[str,Any]:
    return {"level": level, "bundles": LEVELS.get(level, LEVELS["medium"])}
