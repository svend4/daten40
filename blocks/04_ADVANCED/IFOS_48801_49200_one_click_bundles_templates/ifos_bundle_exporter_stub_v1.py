# ifos_bundle_exporter_stub_v1.py
from __future__ import annotations
from typing import Dict

def export(bundle: Dict, fmt: str="zip") -> Dict:
    return {"format":fmt,"outputs":["bundle."+fmt]}
