# ifos_connector_contract_check_stub_v1.py
from __future__ import annotations
from typing import Dict, List

REQUIRED=["connector_id","name","provider","capabilities","auth","resources","limits","version"]

def check(contract: Dict) -> List[str]:
    missing=[k for k in REQUIRED if k not in contract]
    return missing
