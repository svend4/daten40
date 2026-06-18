# ifos_rollback_executor_stub_v1.py
from __future__ import annotations
from typing import Dict

def rollback(promotion_id: str) -> Dict:
    return {"status":"ROLLED_BACK","promotion_id":promotion_id}
