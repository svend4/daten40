# ifos_vault_packager_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def make_pack(files: List[str], hashes: Dict[str,str]) -> Dict:
    return {"files": files, "hashes": hashes}
