# ifos_import_dedup_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def cluster(assets: List[Dict]) -> List[Dict]:
    # placeholder: cluster by first capability
    clusters={}
    for a in assets:
        key=(a.get("capabilities") or ["misc"])[0]
        clusters.setdefault(key, []).append(a.get("asset_id"))
    return [{"cluster_id":f"cl.{k}", "assets":v} for k,v in clusters.items()]
