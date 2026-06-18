# ifos_affiliate_attribution_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def attribute(event: Dict[str, Any]) -> Dict[str, Any]:
    # stub: prefer server-to-server click_id if present
    cid=event.get("click_id") or event.get("cid")
    return {"attributed": bool(cid), "click_id": cid, "window_days": 30}
