# ifos_registry_validator_stub_v1.py
from __future__ import annotations
from typing import Dict, List

REQUIRED=["item_id","name","item_type","summary","capabilities","links","license"]

def validate(item: Dict) -> List[str]:
    missing=[k for k in REQUIRED if k not in item or item.get(k) in (None,"")]
    return missing
