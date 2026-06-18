# ifos_shard_router_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def route(shard_map: Dict[str, Any], tenant_id: str) -> str:
    for rule in shard_map.get("routing", []):
        if rule.get("match", {}).get("tenant_id") == tenant_id:
            return rule.get("to_shard")
    return shard_map.get("shards", [{}])[0].get("shard_id","unknown")
